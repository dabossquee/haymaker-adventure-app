import streamlit as st
import os
import re
import stripe
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. CORE ENGINE PAGE INITIALIZATION
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

# 2. CAPTURE ACTIVE STRIPE PAYWALL REDIRECTS
query_params = st.query_params
if "success" in query_params and query_params["success"] == "true":
    st.session_state.is_premium = True
    st.toast("👑 Premium Unlimited Pass Activated Successfully!")

# 3. SET BASE TRIAL THRESHOLDS & CACHE MEMORY
if "user" not in st.session_state:
    if "guest_tokens" not in st.session_state:
        st.session_state.guest_tokens = 3  # Set to 30 for production release!
    if "world_engine" not in st.session_state:
        st.session_state.world_engine = {
            "world_id": None, "world_name": "", "world_genre": "",
            "player_character": {"name": "", "backstory": "", "health": 100, "inventory": ["survival gear"]},
            "story_log": []
        }
else:
    st.session_state.guest_tokens = 999999  

engine = st.session_state.world_engine
char = engine["player_character"]
# 4. SIDEBAR STATUS OVERWATCH PANEL
with st.sidebar:
    st.title("📊 STATUS CONTROL")
    
    if "user" in st.session_state:
        st.success(f"👑 PREMIUM PILOT: {st.session_state.user.email}")
    else:
        if st.session_state.guest_tokens > 0:
            st.warning(f"⏳ TRIAL ACTIVE: {st.session_state.guest_tokens} Actions Left")
        else:
            st.error("🔒 Action Pool Depleted!")
            
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
        btn_disabled = "user" not in st.session_state and st.session_state.guest_tokens <= 0
        if st.button("🔧 Call Engineer (Heal to 100)", use_container_width=True, disabled=btn_disabled):
            char["health"] = 100
            if "user" not in st.session_state:
                st.session_state.guest_tokens -= 1
            engine["story_log"].append({"role": "user", "content": "🛠️ [System Command] I ordered my engineer to patch the ship hulls!"})
            st.rerun()
    else:
        st.info("No active universe initialized yet. Choose an experience or build one inside the landing tabs.")

# 5. BALA AI LANDING HUB AND PLATFORM NAVIGATION
if not engine["world_name"]:
    st.title("🪐 Haymaker Industry Hub")
    st.subheader("Explore alternate realities or forge your own timeline")
    
    # Render the 5 premium interface navigation tabs cleanly on the main canvas
    tab_explore, tab_my_creations, tab_create, tab_avatars, tab_profile = st.tabs([
        "🪐 Explore Universes", "🏗️ My Creations", "🪄 Create a World", "🎭 Community Avatars", "👤 Account Profile"
    ])
    
    with tab_explore:
        sub_scifi, sub_fantasy, sub_cyberpunk, sub_ai = st.tabs([
            "🚀 Sci-Fi", "🧙 Dark Fantasy", "🏙️ Cyberpunk", "🤖 Community & AI"
        ])
        with sub_scifi:
            st.markdown("### Pre-Made Sci-Fi Realities")
            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### 🚀 SECTOR 7 NOMAD")
                st.caption("Grit, survival, and starship dogfights across an outlaw solar system.")
                if st.button("🎮 Launch Sector 7", use_container_width=True):
                    engine["world_id"] = "pre_scifi_1"
                    engine["world_name"] = "Sector 7 Nomad"
                    engine["world_genre"] = "Sci-Fi"
                    st.rerun()
            with cols[1]:
                st.markdown("#### 🛰️ CHRONOS STATION")
                st.caption("A psychological thriller aboard a deep-space station stuck in a time anomaly.")
                if st.button("🎮 Launch Chronos", use_container_width=True):
                    engine["world_id"] = "pre_scifi_2"
                    engine["world_name"] = "Chronos Station"
                    engine["world_genre"] = "Sci-Fi"
                    st.rerun()
                    
        with sub_fantasy:
            st.markdown("### Pre-Made Dark Fantasy Realities")
            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### 🧛 VAMPIRE NOMAD")
                st.caption("Navigate exile, bloodlines, and dark covens in a gothic world of endless night.")
                if st.button("🎮 Launch Vampire Nomad", use_container_width=True):
                    engine["world_id"] = "pre_fant_1"
                    engine["world_name"] = "Vampire Nomad"
                    engine["world_genre"] = "Dark Fantasy"
                    st.rerun()
            with cols[1]:
                st.markdown("#### ⚔️ ASHELANDS RENEGADE")
                st.caption("A tactical swords-and-sorcery survival gauntlet across a ruined kingdom.")
                if st.button("🎮 Launch Ashelands", use_container_width=True):
                    engine["world_id"] = "pre_fant_2"
                    engine["world_name"] = "Ashelands Renegade"
                    engine["world_genre"] = "Dark Fantasy"
                    st.rerun()

        with sub_cyberpunk:
            st.markdown("### Pre-Made Cyberpunk Realities")
            cols = st.columns(2)
            with cols[0]:
                st.markdown("#### 🏙️ NEO-TOKYO RUNNER")
                st.caption("High-stakes tech espionage, corporate warfare, and neon-lit street racing.")
                if st.button("🎮 Launch Neo-Tokyo", use_container_width=True):
                    engine["world_id"] = "pre_cyber_1"
                    engine["world_name"] = "Neo-Tokyo Runner"
                    engine["world_genre"] = "Cyberpunk"
                    st.rerun()
            with cols[1]:
                st.markdown("#### ⛓️ GRIDLOCK UNDERGROUND")
                st.caption("Hack deep mainframe grids and lead a digital rebellion against mega-corps.")
                if st.button("🎮 Launch Gridlock", use_container_width=True):
                    engine["world_id"] = "pre_cyber_2"
                    engine["world_name"] = "Gridlock Underground"
                    engine["world_genre"] = "Cyberpunk"
                    st.rerun()

        with sub_ai:
            st.markdown("### Community & AI Generated Universes")
            try:
                public_worlds = supabase_client.table("worlds").select("*").order("created_at", desc=True).execute()
                if public_worlds.data:
                    cols = st.columns(3)
                    for index, world_row in enumerate(public_worlds.data):
                        with cols[index % 3]:
                            st.markdown(f"#### 🪐 {world_row['world_name'].upper()}")
                            st.caption(f"🎭 GENRE: {world_row['world_genre']}")
                            if st.button(f"🎮 Enter Universe", key=f"pub_{world_row['id']}", use_container_width=True):
                                engine["world_id"] = world_row["id"]
                                engine["world_name"] = world_row["world_name"]
                                engine["world_genre"] = world_row["world_genre"]
                                st.rerun()
                else:
                    st.info("No player-built alternate universes have been mapped yet. Be the first to spark the cosmos under 'Create a World'!")
            except Exception as e:
                st.error(f"Database Fetch Error: {e}")
            
    with tab_my_creations:
        st.markdown("### 🏗️ Your Private Universes")
        if "user" in st.session_state:
            try:
                my_worlds = supabase_client.table("worlds").select("*").eq("creator_id", st.session_state.user.id).execute()
                if my_worlds.data:
                    for my_row in my_worlds.data:
                        st.markdown(f"- **{my_row['world_name'].upper()}** ({my_row['world_genre']})")
                else:
                    st.info("You haven't deployed any permanent universes yet.")
            except Exception as e:
                st.error(f"Fetch Error: {e}")
        else:
            st.warning("🔒 Please sign in via the 'Account Profile' tab to look inside your private creation vault.")
    with tab_create:
        st.markdown("### 🪄 Universe Architect Form")
        w_name = st.text_input("Name your universe:", placeholder="e.g., Sector 7, Neo-Tokyo")
        w_genre = st.selectbox("Select thematic genre:", ["Sci-Fi", "Dark Fantasy", "Cyberpunk", "Romance", "Other"])
        c_name = st.text_input("Your character's name:")
        c_backstory = st.text_area("Character profile/backstory:")
        
        if st.button("🚀 Deploy and Ignite Core Engine", use_container_width=True):
            if w_name and w_genre and c_name:
                if "user" in st.session_state:
                    try:
                        new_world = supabase_client.table("worlds").insert({
                            "creator_id": st.session_state.user.id,
                            "world_name": w_name,
                            "world_genre": w_genre
                        }).execute()
                        engine["world_id"] = new_world.data[0]["id"]
                    except Exception as e:
                        st.error(f"Table Write Failure: {e}")
                        st.stop()
                
                engine["world_name"] = w_name
                engine["world_genre"] = w_genre
                char["name"] = c_name
                char["backstory"] = c_backstory
                st.rerun()
            else:
                st.warning("⚠️ Fill out the architectural inputs to launch.")
                
        with tab_avatars:
            st.markdown("### 🎭 Community Avatars Portal")
            cols = st.columns(3)
        with cols[0]:
            st.markdown("#### 👤 COMMANDER DIXON")
            st.markdown("❤️ **HP:** `100/100` | 🎒 `Survival Gear`")
            st.caption("*Ex-military tactical operative specializing in high-stakes salvage ops.*")
            st.image("https://unsplash.com", caption="Fan Art Concept Frame")
        with cols[1]:
            st.markdown("#### 👤 NYX THE SHADOW")
            st.markdown("❤️ **HP:** `85/100` | 🎒 `Datapad, Lockpick`")
            st.caption("*Cybernetic network runner operating out of Tokyo's neon underground.*")
            st.image("https://unsplash.com", caption="Fan Art Concept Frame")
        with cols[2]:
            st.markdown("#### 👤 VALERIUS THE EXILE")
            st.markdown("❤️ **HP:** `100/100` | 🎒 `Ancient Blade, Vial`")
            st.caption("*Nomadic bloodline guardian navigating dark medieval covenant wars.*")
            st.image("https://unsplash.com", caption="Fan Art Concept Frame")

                
    with tab_profile:
        st.markdown("### 👤 User Authentication Center")
        if "user" in st.session_state:
            st.success(f"👑 Secure Profile Synchronized: `{st.session_state.user.email}`")
            if st.button("🚪 Log Out of Platform Account", type="primary", use_container_width=True):
                supabase_client.auth.sign_out()
                st.session_state.clear()
                st.rerun()
        else:
            auth_mode = st.radio("Access Control:", ["Create Account", "Sign In"])
            email = st.text_input("Account Email:")
            password = st.text_input("Password:", type="password")
            
            if auth_mode == "Create Account":
                if st.button("🚀 Register and Secure Sandbox Profile", use_container_width=True):
                    try:
                        supabase_client.auth.sign_up({"email": email, "password": password})
                        st.success("✅ Account verified! Please switch to 'Sign In' to authenticate.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            elif auth_mode == "Sign In":
                if st.button("🔓 Authenticate Profile", use_container_width=True):
                    try:
                        session_data = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = session_data.user
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
    st.stop()
# 6. ACTIVE ADVENTURE STORY LAYER
st.title(f"🎬 {engine['world_name'].upper()}")

if "user" in st.session_state and not getattr(st.session_state, 'is_premium', False):
    st.subheader("💳 Activate Subscription")
    st.info("Unlock the $10/week Unlimited Pass to keep playing.")
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
            st.markdown(f"[👉 Click Here to Open Secure Stripe Checkout Page]({checkout_session.url})")
        except Exception as e:
            st.error(f"Stripe Error: {e}")
    st.stop()

if "user" not in st.session_state and st.session_state.guest_tokens <= 0:
    st.error("🛑 Free trial actions fully expended!")
    if st.button("🚀 Create an Account / Sign In to Continue", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.stop()

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
        initial_story = response.choices.message.content
        engine["story_log"].append({"role": "user", "content": "Wake up and look around."})
        engine["story_log"].append({"role": "assistant", "content": initial_story})
        st.rerun()

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
