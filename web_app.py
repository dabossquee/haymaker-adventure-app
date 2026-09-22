import streamlit as st
import os
import re
import stripe
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. INITIALIZE MASTER PAGE ENVIRONMENT
st.set_page_config(page_title="Haymaker Engine", page_icon="🪐", layout="wide")

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_SECRET = os.getenv("STRIPE_SECRET_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not API_KEY or not SUPABASE_URL or not SUPABASE_KEY:
    st.error("🔒 Missing crucial core environment variables inside your hidden .env file!")
    st.stop()

openai_client = OpenAI(api_key=API_KEY)
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if STRIPE_SECRET:
    stripe.api_key = STRIPE_SECRET

# 2. STRIPE CHECKOUT REDIRECT STATE CAPTURE
query_params = st.query_params
if "success" in query_params and query_params["success"] == "true":
    st.session_state.is_premium = True
    st.toast("👑 Premium Unlimited Pass Activated Successfully!")

# 3. SET GENEROUS HOOK THRESHOLDS & ENGINE MEMORY
if "user" not in st.session_state:
    if "guest_tokens" not in st.session_state:
        st.session_state.guest_tokens = 3  # Set to 3 for instant testing. Switch to 30 for production!
    if "world_engine" not in st.session_state:
        st.session_state.world_engine = {
            "world_name": "", "world_genre": "",
            "player_character": {"name": "", "backstory": "", "health": 100, "inventory": ["survival gear"]},
            "story_log": []
        }
else:
    st.session_state.guest_tokens = 999999  

engine = st.session_state.world_engine
char = engine["player_character"]

# 4. SIDEBAR DASHBOARD CONTROL LAYER
with st.sidebar:
    st.title("📊 STATUS CONTROL")
    
    if "user" in st.session_state:
        st.success(f"👑 PREMIUM PILOT: `{st.session_state.user.email}`")
        st.info("⚡ UNLIMITED ADVENTURE MODE ACTIVE")
        if st.button("🚪 Log Out of Session", type="primary", use_container_width=True):
            supabase_client.auth.sign_out()
            st.session_state.clear()
            st.rerun()
    else:
        if st.session_state.guest_tokens > 0:
            st.warning(f"⏳ TRIAL ACTIVE: {st.session_state.guest_tokens} Actions Left")
            st.info("🛡️ Zero Ads. Zero Traps. Experience absolute narrative freedom.")
        else:
            st.subheader("🔒 Action Pool Depleted!")
            st.error("Create an account and unlock the $10/week Unlimited Pass to save your universe timeline.")
            
            auth_mode = st.radio("Access Corridors:", ["Create Account", "Sign In"])
            email = st.text_input("Account Email:")
            password = st.text_input("Password:", type="password")
            
            if auth_mode == "Create Account":
                if st.button("🚀 Register and Secure Character", use_container_width=True):
                    try:
                        supabase_client.auth.sign_up({"email": email, "password": password})
                        st.success("✅ Account verified! Switch to 'Sign In' to authenticate your pass.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            elif auth_mode == "Sign In":
                if st.button("🔓 Authenticate and Paywall", use_container_width=True):
                    try:
                        session_data = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = session_data.user
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            st.stop() 

    st.divider()
    if engine["world_name"]:
        st.markdown(f"**🪐 WORLD:** {engine['world_name'].upper()}")
        st.markdown(f"**🎭 GENRE:** {engine['world_genre'].upper()}")
        st.divider()
        st.markdown(f"### 👤 {char['name']}")
        
        health_pct = max(0, min(100, char["health"]))
        st.progress(health_pct / 100, text=f"❤️ Health Pool: {health_pct}/100")
        
        st.markdown("### 🎒 Inventory Pack")
        for item in char["inventory"]:
            st.markdown(f"- 📦 {item}")
        st.divider()
        
        if "user" in st.session_state and not getattr(st.session_state, 'is_premium', False):
            st.subheader("💳 Activate Subscription")
            if st.button("👑 Get Unlimited Pass ($10/wk)", type="primary", use_container_width=True):
                try:
                    checkout_session = stripe.checkout.Session.create(
                        payment_method_types=['card'],
                        line_items=[{
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {'name': 'Haymaker Unlimited Adventurer Pass'},
                                'unit_amount': 1000, 
                                'recurring': {'interval': 'week'} 
                            },
                            'quantity': 1,
                        }],
                        mode='subscription',
                        success_url='https://onrender.com',
                        cancel_url='https://onrender.com',
                    )
                    st.success("Secure link generated!")
                    st.markdown(f"[👉 Click Here to Open Secure Stripe Checkout Page]({checkout_session.url})")
                except Exception as e:
                    st.error(f"Stripe Gateway Error: {e}")
            st.stop() 

        btn_disabled = "user" not in st.session_state and st.session_state.guest_tokens <= 0
        if st.button("🔧 Call Engineer (Heal to 100)", use_container_width=True, disabled=btn_disabled):
            char["health"] = 100
            if "user" not in st.session_state:
                st.session_state.guest_tokens -= 1
            engine["story_log"].append({"role": "user", "content": "🛠️ [System Command] I ordered my engineer to patch the ship hulls!"})
            st.rerun()

# 5. INITIAL UNIVERSE ARCHITECT ENTRY PANEL
if not engine["world_name"]:
    st.title("🪐 Haymaker Universe Architect")
    st.subheader("Configure your custom universe structure from scratch")
    
    w_name = st.text_input("Name your universe/world:", placeholder="e.g., Mother Earth, Sector 7")
    w_genre = st.text_input("What is the genre?", placeholder="e.g., Dark Fantasy, Cyberpunk, Sci-Fi")
    c_name = st.text_input("What is your character's name?")
    c_backstory = st.text_area("Give your character a quick backstory/role:")
    
    if st.button("🚀 Initialize World Engine", use_container_width=True):
        if w_name and w_genre and c_name:
            engine["world_name"] = w_name
            engine["world_genre"] = w_genre
            char["name"] = c_name
            char["backstory"] = c_backstory
            st.rerun()
        else:
            st.warning("⚠️ Please fill out the configuration profiles to ignite the core.")
    st.stop()

# 6. CINEMATIC NARRATIVE INTERFACE LAYER
st.title(f"🎬 {engine['world_name'].upper()}")

for text_turn in engine["story_log"]:
    if text_turn["role"] == "user":
        if "[System Command]" in text_turn["content"]:
            st.info(text_turn["content"])
        else:
            st.chat_message("user").write(text_turn["content"])
    elif text_turn["role"] == "assistant":
        clean_text = re.sub(r'\[.*?\]', '', text_turn["content"]).strip()
        st.chat_message("assistant").write(clean_text)

if not engine["story_log"]:
    with st.spinner("⏳ Simulating initial cosmos entry scene..."):
        master_prompt = (
            f"You are the master engine for an advanced text game called Haymaker.\n"
            f"The user's world: '{engine['world_name']}' (Genre: '{engine['world_genre']}').\n"
            f"Character: '{char['name']}' (Backstory: '{char['backstory']}').\n"
            f"Current Inventory: {', '.join(char['inventory'])}.\n"
            f"Current Health: {char['health']}/100.\n"
            f"Generate an immersive opening scene. End by prompting them what to do next."
        )
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": master_prompt}, {"role": "user", "content": "Wake up and look around."}],
            max_tokens=450,
            temperature=0.7
        )
        initial_story = response.choices[0].message.content
        engine["story_log"].append({"role": "user", "content": "Wake up and look around."})
        engine["story_log"].append({"role": "assistant", "content": initial_story})
        st.rerun()

# 7. ACTION PROCESSOR ENTRY GATEWAY WITH FAILSAFE CHECKS
if "user" not in st.session_state and st.session_state.guest_tokens <= 0:
    st.error("🛑 Free actions fully expended. Create an account or sign in via the left sidebar to unlock your dashboard timeline parameters!")
else:
    user_action = st.chat_input("Describe your action or speak...")
    
    if user_action:
        if "user" not in st.session_state:
            st.session_state.guest_tokens -= 1
            
        engine["story_log"].append({"role": "user", "content": user_action})
        
        master_prompt = (
            f"You are the master engine for an advanced text-game called Haymaker.\n"
            f"The user's world: '{engine['world_name']}' (Genre: '{engine['world_genre']}').\n"
            f"Character: '{char['name']}' (Backstory: '{char['backstory']}').\n"
            f"Current Inventory: {', '.join(char['inventory'])}.\n"
            f"Current Health: {char['health']}/100.\n\n"
            f"CRITICAL ENGINE RULES:\n"
            f"1. Never break character. Never mention you are an AI model.\n"
            f"2. Immersively narrate cinematic outcomes matching the genre.\n"
            f"3. Maintain strict coherence with the established world, inventory, and character status provided in the current state.\n"
            f"4. For each user action, calculate the impact on '{char['name']}'s health, inventory, and world situation, updating these variables for the next turn.\n"
            f"5. Generate a concise, vivid description of the consequences of the user's choices, ensuring the tone remains intense and engaging.\n\n"
            f"Always append system data tags at the absolute bottom if state changes:\n"
            f"   - Award item: [LOOT: item_name]\n"
            f"   - Modify health: [HEALTH: -15]"
        )
        
        messages = [{"role": "system", "content": master_prompt}]
        for past_turn in engine["story_log"]:
            messages.append({"role": past_turn["role"], "content": past_turn["content"]})
            
        with st.spinner("⏳ Simulating reality consequences..."):
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=450,
                temperature=0.7
            )
            
            raw_ai_text = response.choices.message.content
            
            loot_matches = re.findall(r'\[LOOT:\s*(.*?)\]', raw_ai_text, re.IGNORECASE)
            for item in loot_matches:
                if item.strip() not in char["inventory"]:
                    char["inventory"].append(item.strip())
                    
            health_matches = re.findall(r'\[HEALTH:\s*([+-]\d+)\]', raw_ai_text)
            for modifier in health_matches:
                char["health"] += int(modifier)
                char["health"] = max(0, min(100, char["health"]))
                
            engine["story_log"].append({"role": "assistant", "content": raw_ai_text})
            st.rerun()
