import streamlit as st
import os
import re
import json
import random
import stripe
from openai import OpenAI
from dotenv import load_dotenv

# 1. PAGE SETUP (Forces Modern Dark Mode Theme)
st.set_page_config(page_title="Haymaker Engine", page_icon="🪐", layout="wide")

# Load hidden security environmental variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_SECRET = os.getenv("STRIPE_SECRET_KEY")

if not API_KEY:
    st.error("🔒 Could not find your 'OPENAI_API_KEY' inside the hidden .env file.")
    st.stop()

# Initialize API connections
client = OpenAI(api_key=API_KEY)
if STRIPE_SECRET:
    stripe.api_key = STRIPE_SECRET

SAVE_FILE = "world_save.json"

# 2. INITIALIZE SESSION STATE MEMORY
if "world_engine" not in st.session_state:
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            st.session_state.world_engine = json.load(f)
    else:
        st.session_state.world_engine = {
            "world_name": "",
            "world_genre": "",
            "player_character": {
                "name": "",
                "backstory": "",
                "health": 100,
                "inventory": ["survival gear"]
            },
            "story_log": []
        }

if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

engine = st.session_state.world_engine
char = engine["player_character"]

def save_state():
    with open(SAVE_FILE, "w") as f:
        json.dump(st.session_state.world_engine, f, indent=4)

# 3. INTERACTIVE VISUAL SETUP INTERFACE
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
            save_state()
            st.rerun()
        else:
            st.warning("⚠️ Please fill out the configuration profiles to ignite the core.")
    st.stop()

# 4. SIDEBAR DASHBOARD DISPLAY (With Live Stripe Paywall)
with st.sidebar:
    st.title("📊 STATUS CONTROL")
    st.markdown(f"**🪐 WORLD:** {engine['world_name'].upper()}")
    st.markdown(f"**🎭 GENRE:** {engine['world_genre'].upper()}")
    st.divider()
    
    # STRIPE GATEWAY GATE: If they aren't premium, give them an active purchase portal button
    if not st.session_state.is_premium:
        st.subheader("👑 Haymaker Premium")
        st.info("Unlock infinite actions, custom character traits, and advanced AI mechanics.")
        
        # Simulated developer payment router using raw Stripe Checkout Session URLs
        if st.button("💳 Upgrade for $4.99/mo", type="primary", use_container_width=True):
            if not STRIPE_SECRET:
                st.error("Missing STRIPE_SECRET_KEY in your .env file!")
            else:
                try:
                    # Tells Stripe to build a hosted checkout page automatically
                    checkout_session = stripe.checkout.Session.create(
                        payment_method_types=['card'],
                        line_items=[{
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {'name': 'Haymaker Adventurer Pass'},
                                'unit_amount': 499,
                                'recurring': {'interval': 'month'}
                            },
                            'quantity': 1,
                        }],
                        mode='subscription',
                        success_url='http://localhost:8501/?success=true',
                        cancel_url='http://localhost:8501/?cancel=true',
                    )
                    # Force local simulation override for prototype testing
                    st.session_state.is_premium = True
                    st.success("Redirecting to safe testing checkout gateway...")
                    st.markdown(f"[Click here to go to your live Stripe payment page]({checkout_session.url})")
                except Exception as e:
                    st.error(f"Stripe Error: {e}")
    else:
        st.success("👑 PREMIUM ACCOUNT ACTIVE")
        
    st.divider()
    st.markdown(f"### 👤 {char['name']}")
    
    health_pct = max(0, min(100, char["health"]))
    st.progress(health_pct / 100, text=f"❤️ Health Pool: {health_pct}/100")
    
    st.markdown("### 🎒 Inventory Pack")
    for item in char["inventory"]:
        st.markdown(f"- 📦 {item}")
        
    st.divider()
    st.markdown("### ⚡ TACTICAL COMMANDS")
    if st.button("🔧 Call Engineer (Heal to 100)", use_container_width=True):
        char["health"] = 100
        save_state()
        engine["story_log"].append({"role": "user", "content": "🛠️ [System Command] I ordered my engineer to patch the ship hulls!"})
        st.rerun()

    if st.button("❌ Wipe Save & Reset", type="primary", use_container_width=True):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        st.session_state.clear()
        st.rerun()

# 5. THE ACTIVE ADVENTURE DISPLAY
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
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": master_prompt}, {"role": "user", "content": "Wake up and look around."}],
            max_tokens=450,
            temperature=0.7
        )
        initial_story = response.choices[0].message.content
        engine["story_log"].append({"role": "user", "content": "Wake up and look around."})
        engine["story_log"].append({"role": "assistant", "content": initial_story})
        save_state()
        st.rerun()

# 6. ACTION PROCESSING PIPELINE
user_action = st.chat_input("Describe your action or speak...")

if user_action:
    # Action limit check if not premium (simulating a monetized paywall tier)
    user_turns = len([t for t in engine["story_log"] if t["role"] == "user" and t["content"] != "Wake up and look around."])
    if user_turns >= 5 and not st.session_state.is_premium:
        st.error("🛑 Action limit reached for free trial! Please upgrade in the sidebar to keep playing your story.")
    else:
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
            f"3. Always append system data tags at the absolute bottom if state changes:\n"
            f"   - Award item: [LOOT: item_name]\n"
            f"   - Modify health: [HEALTH: -15]"
        )
        
        messages = [{"role": "system", "content": master_prompt}]
        for past_turn in engine["story_log"]:
            messages.append({"role": past_turn["role"], "content": past_turn["content"]})
            
        with st.spinner("⏳ Simulating reality consequences..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=450,
                temperature=0.7
            )
            
            raw_ai_text = response.choices[0].message.content
            
            loot_matches = re.findall(r'\[LOOT:\s*(.*?)\]', raw_ai_text, re.IGNORECASE)
            for item in loot_matches:
                if item.strip() not in char["inventory"]:
                    char["inventory"].append(item.strip())
                    
            health_matches = re.findall(r'\[HEALTH:\s*([+-]\d+)\]', raw_ai_text)
            for modifier in health_matches:
                char["health"] += int(modifier)
                char["health"] = max(0, min(100, char["health"]))
                
            engine["story_log"].append({"role": "assistant", "content": raw_ai_text})
            save_state()
            st.rerun()
