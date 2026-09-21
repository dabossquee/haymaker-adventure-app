import streamlit as st
import os
import re
import stripe
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. PAGE SETUP & SECURITY INITIALIZATION
st.set_page_config(page_title="Haymaker Engine", page_icon="🪐", layout="wide")

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_SECRET = os.getenv("STRIPE_SECRET_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not API_KEY or not SUPABASE_URL or not SUPABASE_KEY:
    st.error("🔒 Missing crucial core environment variables inside your hidden .env file!")
    st.stop()

# Initialize API client infrastructure cleanly
openai_client = OpenAI(api_key=API_KEY)
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if STRIPE_SECRET:
    stripe.api_key = STRIPE_SECRET

# 2. SEPARATE LOG IN & SIGN UP GATEWAY
if "user" not in st.session_state:
    st.title("🪐 Haymaker Industry Engine")
    st.subheader("Layer 1 Authentication: Access Your Private Universe")
    
    auth_mode = st.radio("Choose operational access profile:", ["Sign In", "Create Account"])
    email = st.text_input("Enter your account email:")
    password = st.text_input("Enter password:", type="password")
    
    if auth_mode == "Create Account":
        if st.button("🚀 Register New Sandbox Account", use_container_width=True):
            try:
                # Creates user natively in Supabase's managed Auth tables
                response = supabase_client.auth.sign_up({"email": email, "password": password})
                st.success("✅ Account created successfully! Please switch to 'Sign In' and enter your universe.")
            except Exception as e:
                st.error(f"Registration Error: {e}")
                
    elif auth_mode == "Sign In":
        if st.button("🔓 Authenticate and Enter", use_container_width=True):
            try:
                # Verifies password hash securely
                session_data = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = session_data.user
                st.rerun()
            except Exception as e:
                st.error(f"Authentication Failure: {e}")
    st.stop()

# 3. CONFIGURE RUNTIME USER VARIABLES
user_id = st.session_state.user.id

# Initialize single-session memory profile (Upgrading to tables tomorrow)
if "world_engine" not in st.session_state:
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

# 4. SIDEBAR DASHBOARD DISPLAY (Isolated to Active Session)
with st.sidebar:
    st.title("📊 STATUS CONTROL")
    st.markdown(f"**👤 LOGGED IN AS:** `{st.session_state.user.email}`")
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
        st.markdown("### ⚡ TACTICAL COMMANDS")
        if st.button("🔧 Call Engineer (Heal to 100)", use_container_width=True):
            char["health"] = 100
            engine["story_log"].append({"role": "user", "content": "🛠️ [System Command] I ordered my engineer to patch the ship hulls!"})
            st.rerun()
            
    if st.button("🚪 Log Out of Session", type="primary", use_container_width=True):
        # Clears active token memory out cleanly
        supabase_client.auth.sign_out()
        st.session_state.clear()
        st.rerun()

# 5. USER UNIVERSE CONFIGURATION DESIGN
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

# 6. ACTIVE ADVENTURE STORY LAYER
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

user_action = st.chat_input("Describe your action or speak...")

if user_action:
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
        response = openai_client.chat.completions.create(
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
        st.rerun()
