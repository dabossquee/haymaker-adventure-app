"""
Stripe webhook service. Deploy as a SEPARATE web service (Streamlit cannot receive webhooks).

Start command:  uvicorn stripe_webhook:app --host 0.0.0.0 --port $PORT
requirements:   fastapi, uvicorn[standard], stripe, supabase

Env vars (this service only; never put the service key in the Streamlit app):
  STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, SUPABASE_URL, SUPABASE_SERVICE_KEY
"""
import json
import os
import logging

import stripe
from fastapi import FastAPI, HTTPException, Request
from supabase import create_client

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]
db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])

log = logging.getLogger("stripe_webhook")
app = FastAPI()

# past_due keeps access while Stripe retries the card (grace period).
# Access is revoked when Stripe gives up (unpaid / canceled / incomplete_expired).
ACCESS_STATUSES = {"active", "trialing", "past_due"}


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
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # 2. Work with plain dicts from here on
    event = json.loads(payload)
    etype = event["type"]
    obj = event["data"]["object"]

    # Any exception below returns HTTP 500, so Stripe retries the event.
    if etype == "checkout.session.completed":
        if obj.get("mode") != "subscription":
            return {"ok": True}
        user_id = obj.get("client_reference_id")
        if not user_id:
            log.warning("checkout.session.completed without client_reference_id: %s", obj.get("id"))
            return {"ok": True}
        db.table("profiles").update({
            "is_premium": True,
            "stripe_customer_id": obj.get("customer"),
            "stripe_subscription_id": obj.get("subscription"),
            "subscription_status": "active",
            "tier": (obj.get("metadata") or {}).get("tier"),
        }).eq("id", user_id).execute()

    elif etype in ("customer.subscription.updated", "customer.subscription.deleted"):
        status = "canceled" if etype.endswith("deleted") else obj.get("status")
        db.table("profiles").update({
            "is_premium": status in ACCESS_STATUSES,
            "subscription_status": status,
        }).eq("stripe_customer_id", obj.get("customer")).execute()

    elif etype == "invoice.paid":
        db.table("profiles").update({
            "is_premium": True,
            "subscription_status": "active",
        }).eq("stripe_customer_id", obj.get("customer")).execute()

    elif etype == "invoice.payment_failed":
        # Status only; subscription.updated decides when access is actually revoked
        db.table("profiles").update({
            "subscription_status": "past_due",
        }).eq("stripe_customer_id", obj.get("customer")).execute()

    return {"ok": True}