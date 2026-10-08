"""
Haymaker Stripe webhook service. Runs as its OWN web service (Streamlit cannot receive webhooks).

Render settings
  Build Command:  pip install --upgrade pip && pip install "fastapi>=0.110,<1.0" "uvicorn[standard]>=0.29,<1.0" "stripe>=10.0" "supabase>=2.9,<3.0"
  Start Command:  uvicorn stripe_webhook:app --host 0.0.0.0 --port $PORT

Environment variables (this service only; the service key must never be put in the Streamlit app)
  STRIPE_WEBHOOK_SECRET   the signing secret (whsec_...) of THIS endpoint in Stripe, test or live to match
  SUPABASE_URL            your project URL
  SUPABASE_SERVICE_KEY    the service_role / secret key
  STRIPE_SECRET_KEY       sk_test_... / sk_live_... (needed by Cancel Subscription and by sync; webhooks work without it)

Plans (all three give the same access; only the billing period differs)
  weekly    Weekly Premium Pass            $10 / week
  explorer  6-Month Explorer Pass          $50 / 6 months
  legend    1-Year Ultimate Legend Pass    $100 / year

What it writes (table public.profiles)
  is_premium, tier (weekly / explorer / legend), subscription_status ("active", "past_due", "cancelled", ...),
  stripe_customer_id, stripe_subscription_id and premium_until (the end of the period that has been paid for).

Endpoints
  POST /stripe/webhook        called by Stripe
  POST /subscription/cancel   called by the app: "Authorization: Bearer <the person's Supabase access token>".
                              Cancels at the END of the paid period, marks the profile "cancelled", keeps access until then.
  POST /subscription/sync     called by the app (same Bearer token, optional ?session_id=cs_...).
                              Asks Stripe what this person has paid for and saves it in profiles, so a paid pass is never
                              "forgotten" even if a Stripe event was missed. Only subscriptions that provably belong to the
                              person are used: their checkout session, their id tag, or the customer already linked to them.
"""
import json
import logging
import os
from datetime import datetime, timezone

import stripe
from fastapi import FastAPI, Header, HTTPException, Request
from supabase import create_client

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("stripe_webhook")


def _require(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing environment variable {name}. Add it in Render > Environment and redeploy.")
    return value


WEBHOOK_SECRET = _require("STRIPE_WEBHOOK_SECRET")
db = create_client(_require("SUPABASE_URL"), _require("SUPABASE_SERVICE_KEY"))
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "").strip() or None
app = FastAPI()

PLANS = ("weekly", "explorer", "legend")
PLAN_BY_INTERVAL = {("week", 1): "weekly", ("month", 6): "explorer", ("year", 1): "legend"}
PLAN_BY_CENTS = {1000: "weekly", 5000: "explorer", 10000: "legend"}

# past_due keeps access while Stripe retries the card (grace period).
# Access is revoked when Stripe gives up (unpaid / canceled / incomplete_expired).
ACCESS_STATUSES = {"active", "trialing", "past_due"}


# ---------------------------------------------------------------- reading Stripe's data
# Stripe has changed where some fields live between API versions, so each value is looked for in every known place.
def as_dict(value):
    return value if isinstance(value, dict) else {}


def clean_plan(value):
    return value if value in PLANS else None


def plan_from_price(price):
    """Work out the plan from a price object: billing interval first, amount as a fallback."""
    price = as_dict(price)
    recurring = as_dict(price.get("recurring"))
    key = (recurring.get("interval"), recurring.get("interval_count") or 1)
    if key in PLAN_BY_INTERVAL:
        return PLAN_BY_INTERVAL[key]
    return PLAN_BY_CENTS.get(price.get("unit_amount"))


def metadata_value(obj, key):
    """Our own tags (tier, user_id) are copied onto the invoice or subscription: find them wherever they landed."""
    places = [
        as_dict(obj.get("metadata")),
        as_dict(as_dict(obj.get("subscription_details")).get("metadata")),
        as_dict(as_dict(as_dict(obj.get("parent")).get("subscription_details")).get("metadata")),
    ]
    for line in as_dict(obj.get("lines")).get("data") or []:
        places.append(as_dict(as_dict(line).get("metadata")))
    for place in places:
        if place.get(key):
            return place[key]
    return None


def plan_of(obj):
    """Plan for an invoice or a subscription: our tier tag first, then the price it was billed with."""
    plan = clean_plan(metadata_value(obj, "tier"))
    if plan:
        return plan
    for line in as_dict(obj.get("lines")).get("data") or []:
        plan = plan_from_price(as_dict(line).get("price")) or plan_from_price(as_dict(line).get("plan"))
        if plan:
            return plan
    for item in as_dict(obj.get("items")).get("data") or []:
        plan = plan_from_price(as_dict(item).get("price")) or plan_from_price(as_dict(item).get("plan"))
        if plan:
            return plan
    return None


def to_iso(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp), tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return None


def paid_until(obj):
    """The end of the period that this invoice or subscription pays for, as an ISO time (or None)."""
    ends = []
    for line in as_dict(obj.get("lines")).get("data") or []:
        ends.append(as_dict(as_dict(line).get("period")).get("end"))
    ends.append(obj.get("current_period_end"))
    for item in as_dict(obj.get("items")).get("data") or []:
        ends.append(as_dict(item).get("current_period_end"))
    ends = [int(e) for e in ends if isinstance(e, (int, float))]
    return to_iso(max(ends)) if ends else None


def subscription_id_of(obj):
    return obj.get("subscription") or as_dict(as_dict(obj.get("parent")).get("subscription_details")).get("subscription")


# ---------------------------------------------------------------- writing to Supabase
def save(fields, user_id=None, customer_id=None, label=""):
    """Write to profiles. With a user id the row is created if it is missing; otherwise the customer id finds it."""
    fields = {k: v for k, v in fields.items() if v is not None}
    if user_id:
        res = db.table("profiles").upsert({"id": user_id, **fields}, on_conflict="id").execute()
    elif customer_id:
        res = db.table("profiles").update(fields).eq("stripe_customer_id", customer_id).execute()
    else:
        log.warning("%s: neither a user id nor a customer id, nothing saved", label)
        return 0
    rows = len(res.data or [])
    log.info("%s -> %d profile row(s) written (%s)", label, rows, ", ".join(sorted(fields)))
    if rows == 0:
        log.warning("%s: no matching profile (customer %s, user %s)", label, customer_id, user_id)
    return rows


def process_event(etype, obj):
    """Apply one verified Stripe event. Anything raised here makes Stripe retry the event later."""
    if etype == "checkout.session.completed":
        if obj.get("mode") != "subscription":
            return "ignored (not a subscription)"
        user_id = obj.get("client_reference_id")
        if not user_id:
            log.warning("checkout.session.completed without client_reference_id: %s", obj.get("id"))
            return "ignored (no user id)"
        save({
            "is_premium": True,
            "subscription_status": "active",
            "stripe_customer_id": obj.get("customer"),
            "stripe_subscription_id": obj.get("subscription"),
            "tier": clean_plan(as_dict(obj.get("metadata")).get("tier")),
        }, user_id=user_id, label=etype)  # premium_until comes from invoice.paid, which has the exact period
        return "premium granted"

    if etype == "invoice.paid":
        save({
            "is_premium": True,
            "subscription_status": "active",
            "stripe_customer_id": obj.get("customer"),
            "stripe_subscription_id": subscription_id_of(obj),
            "tier": plan_of(obj),
            "premium_until": paid_until(obj),
        }, user_id=metadata_value(obj, "user_id"), customer_id=obj.get("customer"), label=etype)
        return "period paid"

    if etype in ("customer.subscription.updated", "customer.subscription.deleted"):
        status = "canceled" if etype.endswith("deleted") else obj.get("status")
        access = status in ACCESS_STATUSES
        # Cancelled at period end: Stripe still says "active" until the period runs out, so the flag decides what we store
        shown = "cancelled" if (status == "canceled" or (access and obj.get("cancel_at_period_end"))) else status
        save({
            "is_premium": access,
            "subscription_status": shown,
            "tier": plan_of(obj),
            "premium_until": paid_until(obj) if access else None,
        }, user_id=metadata_value(obj, "user_id"), customer_id=obj.get("customer"), label=etype)
        return "subscription " + str(shown)

    if etype == "invoice.payment_failed":
        # Status only; subscription.updated decides when access is actually revoked
        save({"subscription_status": "past_due"}, user_id=metadata_value(obj, "user_id"),
             customer_id=obj.get("customer"), label=etype)
        return "marked past_due"

    return "ignored"


# ---------------------------------------------------------------- cancel subscription (called by the app)
def user_from_token(token):
    """(user id, email) of the person this Supabase access token belongs to, or (None, None).
    The caller never tells us who they are."""
    try:
        user = getattr(db.auth.get_user(token), "user", None)
        return getattr(user, "id", None), getattr(user, "email", None)
    except Exception as e:
        log.warning("token check failed: %r", e)
        return None, None


def user_id_from_token(token):
    return user_from_token(token)[0]


def cancel_for_user(user_id):
    """Stop this person's subscription from renewing; they keep access until the end of the period they paid for.
    Returns (http status, payload)."""
    if not stripe.api_key:
        log.error("STRIPE_SECRET_KEY is not set on this service: cancelling is unavailable")
        return 503, {"detail": "Cancelling is not configured"}
    rows = (db.table("profiles").select("stripe_subscription_id,stripe_customer_id")
            .eq("id", user_id).limit(1).execute().data or [])
    if not rows:
        return 404, {"detail": "No profile for this account"}
    sub_id = rows[0].get("stripe_subscription_id")
    customer_id = rows[0].get("stripe_customer_id")
    try:
        if not sub_id and customer_id:  # older rows: find the subscription through the customer
            found = stripe.Subscription.list(customer=customer_id, status="active", limit=1)
            if found["data"]:
                sub_id = found["data"][0]["id"]
        if not sub_id:
            return 404, {"detail": "No active subscription"}
        sub = as_dict(stripe.Subscription.modify(sub_id, cancel_at_period_end=True))
    except Exception as e:
        log.error("Stripe could not cancel %s for user %s: %r", sub_id, user_id, e)
        return 502, {"detail": "Stripe could not cancel the subscription"}
    until = paid_until(sub)
    fields = {"subscription_status": "cancelled", "stripe_subscription_id": sub_id, "premium_until": until}
    db.table("profiles").update({k: v for k, v in fields.items() if v is not None}).eq("id", user_id).execute()
    log.info("user %s cancelled %s at period end (access until %s)", user_id, sub_id, until)
    return 200, {"ok": True, "status": "cancelled", "access_until": until}


@app.post("/subscription/cancel")
def cancel_subscription(authorization: str = Header(default="")):
    token = authorization[7:].strip() if authorization.lower().startswith("bearer ") else ""
    user_id = user_id_from_token(token) if token else None
    if not user_id:
        raise HTTPException(status_code=401, detail="Please sign in again")
    status, payload = cancel_for_user(user_id)
    if status != 200:
        raise HTTPException(status_code=status, detail=payload["detail"])
    return payload


# ---------------------------------------------------------------- sync with Stripe (called by the app)
def apply_subscription(user_id, sub):
    """Save what Stripe says about one subscription in the profile, using the same rules as the webhook events."""
    sub = as_dict(sub)
    status = sub.get("status")
    access = status in ACCESS_STATUSES
    shown = "cancelled" if (status == "canceled" or (access and sub.get("cancel_at_period_end"))) else status
    customer = sub.get("customer")
    customer = customer.get("id") if isinstance(customer, dict) else customer
    save({
        "is_premium": access,
        "subscription_status": shown,
        "stripe_customer_id": customer,
        "stripe_subscription_id": sub.get("id"),
        "tier": plan_of(sub),
        "premium_until": paid_until(sub) if access else None,
    }, user_id=user_id, label="sync")
    return access


def find_user_subscription(user_id, email, profile):
    """The best subscription that provably belongs to this person: tagged with their id, or on the customer that is
    already linked to their profile. An email address alone is never enough."""
    linked = profile.get("stripe_customer_id")
    customer_ids = [linked] if linked else []
    if email:
        for customer in stripe.Customer.list(email=email, limit=5)["data"]:
            if customer["id"] not in customer_ids:
                customer_ids.append(customer["id"])
    best = None
    for customer_id in customer_ids:
        for sub in stripe.Subscription.list(customer=customer_id, status="all", limit=10)["data"]:
            mine = as_dict(sub.get("metadata")).get("user_id") == user_id or customer_id == linked
            if not mine:
                continue
            rank = (sub.get("status") in ACCESS_STATUSES, paid_until(sub) or "")
            if best is None or rank > best[0]:
                best = (rank, sub)
    return best[1] if best else None


def sync_for_user(user_id, email, session_id=""):
    """Reconcile one account with Stripe. Returns (http status, payload)."""
    if not stripe.api_key:
        log.error("STRIPE_SECRET_KEY is not set on this service: syncing is unavailable")
        return 503, {"detail": "Syncing is not configured"}
    rows = db.table("profiles").select("stripe_subscription_id,stripe_customer_id").eq("id", user_id).limit(1).execute().data or []
    profile = rows[0] if rows else {}
    try:
        sub = None
        if session_id:  # coming back from checkout: that exact payment
            cs = as_dict(stripe.checkout.Session.retrieve(session_id, expand=["subscription"]))
            if cs.get("client_reference_id") != user_id or cs.get("mode") != "subscription" or cs.get("status") != "complete":
                return 403, {"detail": "That checkout does not belong to this account"}
            sub = cs.get("subscription")
            if isinstance(sub, str):
                sub = stripe.Subscription.retrieve(sub)
        if sub is None:
            sub = find_user_subscription(user_id, email, profile)
        if sub is None:
            return 200, {"ok": True, "found": False, "premium": False}
        premium = apply_subscription(user_id, sub)
    except Exception as e:
        log.error("sync failed for user %s: %r", user_id, e)
        return 502, {"detail": "Stripe could not be reached"}
    log.info("user %s synced with Stripe (premium=%s)", user_id, premium)
    return 200, {"ok": True, "found": True, "premium": premium}


@app.post("/subscription/sync")
def sync_subscription(authorization: str = Header(default=""), session_id: str = ""):
    token = authorization[7:].strip() if authorization.lower().startswith("bearer ") else ""
    user_id, email = user_from_token(token) if token else (None, None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Please sign in again")
    status, payload = sync_for_user(user_id, email, session_id)
    if status != 200:
        raise HTTPException(status_code=status, detail=payload["detail"])
    return payload


# ---------------------------------------------------------------- web service
@app.get("/")
@app.get("/health")
def health():
    return {"ok": True}


@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")

    # 1. Verify the request really came from Stripe
    try:
        stripe.Webhook.construct_event(payload, signature, WEBHOOK_SECRET)
    except Exception as e:
        log.error("signature check failed (wrong STRIPE_WEBHOOK_SECRET for this mode?): %r", e)
        raise HTTPException(status_code=400, detail="Invalid signature")

    # 2. Work with plain dicts from here on
    event = json.loads(payload)
    etype = event["type"]
    log.info("received %s (%s)", etype, event.get("id"))
    outcome = process_event(etype, as_dict(as_dict(event.get("data")).get("object")))
    log.info("%s: %s", etype, outcome)
    return {"ok": True}