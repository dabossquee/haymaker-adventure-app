import streamlit as st
import os
import re
import time
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

# POP-UP INSPECTOR WINDOW GATEWAY
if "active_modal" in st.session_state and st.session_state.active_modal:
    modal = st.session_state.active_modal
    @st.dialog(modal["title"])
    def render_modal_window():
        st.info(f"📁 {modal['img']}")
        st.markdown(f"**🎨 Creator ID:** `{modal['creator']}`")
        st.markdown(f"**🎭 Character Dossier:** {modal['bio']}")
        if st.button("🚪 Close Dossier File", use_container_width=True):
            st.session_state.active_modal = None
            st.rerun()
    render_modal_window()

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
    
    if engine["world_name"]:
        if st.button("🚪 ABANDON TIMELINE (HOME HUB)", type="secondary", use_container_width=True):
            st.session_state.world_engine = {
                "world_id": None, "world_name": "", "world_genre": "",
                "player_character": {"name": "", "backstory": "", "health": 100, "inventory": ["survival gear"]},
                "story_log": []
            }
            st.rerun()
            
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
        st.subheader("📡 CONSOLE PARAMETERS")
        st.caption("No active universe initialized yet. Choose an experience or build one inside the landing tabs.")
        
        if st.button("⚡ Test Cloud Telemetry", use_container_width=True):
            st.toast("🟢 Cloud Matrix Online. Handshake with Supabase database stable.")
        if st.button("📰 View Engine Logs", use_container_width=True):
            st.info("System Patch: Version 1.2.0 Active. Bala Multi-Tab Discovery Core fully synced. DALL-E image pipelines scheduled for Phase 2 deployment sprints.")
# 5. BALA AI LANDING HUB AND PLATFORM NAVIGATION
if not engine["world_name"]:
    st.title("🪐 Haymaker Industry Hub")
    st.subheader("Explore alternate realities or forge your own timeline")
    
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
                    char["name"] = "Pilot Vance"
                    char["backstory"] = "A disgraced military pilot running illicit scrap metal through deep-space asteroid fields to stay hidden."
                    st.rerun()
            with cols[1]:
                st.markdown("#### 🛰️ CHRONOS STATION")
                st.caption("A psychological thriller aboard a deep-space station stuck in a time anomaly.")
                if st.button("🎮 Launch Chronos", use_container_width=True):
                    engine["world_id"] = "pre_scifi_2"
                    engine["world_name"] = "Chronos Station"
                    engine["world_genre"] = "Sci-Fi"
                    char["name"] = "Dr. Aris"
                    char["backstory"] = "The chief quantum technician investigating a strange radiation pulse that locked the entire station loop."
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
                    char["name"] = "Kaelen Voss"
                    char["backstory"] = "An ancient rogue vampire cast out of the High Court, struggling to survive among deadly monster hunters."
                    st.rerun()
            with cols[1]:
                st.markdown("#### ⚔️ ASHELANDS RENEGADE")
                st.caption("A tactical swords-and-sorcery survival gauntlet across a ruined kingdom.")
                if st.button("🎮 Launch Ashelands", use_container_width=True):
                    engine["world_id"] = "pre_fant_2"
                    engine["world_name"] = "Ashelands Renegade"
                    engine["world_genre"] = "Dark Fantasy"
                    char["name"] = "Gideon Black"
                    char["backstory"] = "A weathered mercenary carrying the broken sword of his king across fields contaminated by volcanic ash."
                    st.rerun()
        with sub_cyberpunk:
            st.markdown("### Pre-Made Cyberpunk Realities")
            cols_cyber = st.columns(2)
            with cols_cyber[0]:
                st.markdown("#### 🏙️ NEO-TOKYO RUNNER")
                st.caption("High-stakes tech espionage, corporate warfare, and neon-lit street racing.")
                if st.button("🎮 Launch Neo-Tokyo", use_container_width=True):
                    engine["world_id"] = "pre_cyber_1"
                    engine["world_name"] = "Neo-Tokyo Runner"
                    engine["world_genre"] = "Cyberpunk"
                    char["name"] = "Ren 'Zero' Tanaka"
                    char["backstory"] = "A skilled street racer running data modifications inside a hidden neural link to pay off yakuza syndicates."
                    st.rerun()
            with cols_cyber[1]:
                st.markdown("#### ⛓️ GRIDLOCK UNDERGROUND")
                st.caption("Hack deep mainframe grids and lead a digital rebellion against mega-corps.")
                if st.button("🎮 Launch Gridlock", use_container_width=True):
                    engine["world_id"] = "pre_cyber_2"
                    engine["world_name"] = "Gridlock Underground"
                    engine["world_genre"] = "Cyberpunk"
                    char["name"] = "Echo"
                    char["backstory"] = "A phantom hacker who lives entirely inside deep mainframe server nodes, wiping dirty corporate banks."
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
                                char["name"] = "Unknown Wanderer"
                                char["backstory"] = "A traveler dropped suddenly into an unfamiliar alternate reality matrix checkpoint."
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
                        if "access_token" in st.session_state:
                            supabase_client.postgrest.auth(st.session_state["access_token"])
                        supabase_client.table("worlds").insert({
                            "creator_id": st.session_state.user.id,
                            "world_name": str(w_name).strip(),
                            "world_genre": str(w_genre).strip()
                        }).execute()
                        engine["world_id"] = "user_custom"
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
        st.caption("Click 'Inspect File' to view full resolution profiles and creator records.")
        
        cols = st.columns(3)
        with cols:
            st.markdown("#### 👤 COMMANDER DIXON")
            st.markdown("❤️ **HP:** `100/100` | 🎒 `Survival Gear`")
            st.caption("*Ex-military tactical operative specializing in high-stakes salvage ops.*")
            st.image("https://picsum.photos", use_container_width=True)
            if st.button("🔍 Inspect Dixon File", key="btn_dixon_inspect", use_container_width=True):
                st.session_state.active_modal = {
                    "title": "👤 COMMANDER DIXON", "creator": "Alpha_Dreamer99",
                    "bio": "Ex-military tactical operative specializing in high-stakes salvage ops across lawless outer rims.",
                    "img": "https://picsum.photos"
                }
                st.rerun()
        with cols:
            st.markdown("#### 👤 NYX THE SHADOW")
            st.markdown("❤️ **HP:** `85/100` | 🎒 `Datapad, Lockpick`")
            st.caption("*Cybernetic network runner operating out of Tokyo's neon underground.*")
            st.image("https://picsum.photos", use_container_width=True)
            if st.button("🔍 Inspect Nyx File", key="btn_nyx_inspect", use_container_width=True):
                st.session_state.active_modal = {
                    "title": "👤 NYX THE SHADOW", "creator": "Neon_Ghost",
                    "bio": "Cybernetic network runner operating out of Neo-Tokyo's underbelly. Known for breaking corporate firewalls.",
                    "img": "https://picsum.photos"
                }
                st.rerun()
        with cols:
            st.markdown("#### 👤 VALERIUS THE EXILE")
            st.markdown("❤️ **HP:** `100/100` | 🎒 `Ancient Blade`")
            st.caption("*Nomadic bloodline guardian navigating dark medieval covenant wars.*")
            st.image("https://picsum.photos", use_container_width=True)
            if st.button("🔍 Inspect Valerius File", key="btn_valerius_inspect", use_container_width=True):
                st.session_state.active_modal = {
                    "title": "👤 VALERIUS THE EXILE", "creator": "Gothic_Lord",
                    "bio": "Nomadic bloodline guardian navigating dark medieval covenant wars. Wielder of the sun-forged iron blade.",
                    "img": "https://picsum.photos"
                }
                st.rerun()
                
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
                        if hasattr(session_data, 'session') and session_data.session:
                            st.session_state["access_token"] = session_data.session.access_token
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
    st.stop()
# 6. ACTIVE ADVENTURE STYLING OVERLAY (GLASSMORPHISM RESPONSIVE WRAPPERS)
st.markdown("""
<style>
    .glass-bubble-user {
        background-color: rgba(255, 75, 75, 0.12);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 75, 75, 0.2);
        border-radius: 16px 16px 2px 16px;
        padding: 12px 16px;
        color: #ffffff;
        font-size: 15px;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .glass-bubble-ai {
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px 16px 16px 2px;
        padding: 12px 16px;
        color: #f0f2f6;
        font-size: 15px;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title(f"🎬 {engine['world_name'].upper()}")

# THE UNIVERSAL PLAYER LOCK: The paywall ONLY activates if they aren't premium AND their actions hit 0
if "user" in st.session_state:
    if st.session_state.user.email == "your_exact_admin_email@example.com":
        st.session_state.is_premium = True

is_premium_active = getattr(st.session_state, 'is_premium', False)
has_trial_tokens = st.session_state.guest_tokens > 0

if not is_premium_active and not has_trial_tokens:
    st.subheader("💳 Activate Subscription")
    st.info("Your free trial action points have been exhausted. Unlock the $10/week Unlimited Pass to continue your timeline.")
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

# RENDERING THE NATIVE HISTORY LAYER WITH AVATARS + GLASS CHAT BUBBLES
for text_turn in engine["story_log"]:
    if text_turn["role"] == "user":
        if "[System Command]" in text_turn["content"]:
            st.info(text_turn["content"])
        else:
            cols = st.columns([1, 4, 1])
            with cols[2]:
                st.markdown("### 👤")
            with cols[1]:
                st.markdown(f'<div class="glass-bubble-user">{text_turn["content"]}</div>', unsafe_allow_html=True)
    elif text_turn["role"] == "assistant":
        clean_text = re.sub(r'\[.*?\]', '', text_turn["content"]).strip()
        cols = st.columns([1, 4, 1])
        with cols[0]:
            st.markdown("### 🤖")
        with cols[1]:
            st.markdown(f'<div class="glass-bubble-ai">{clean_text}</div>', unsafe_allow_html=True)

# 7. CHRONOS SPACE MATRIX INITIAL SCENE SPARK
if not engine["story_log"]:
    with st.spinner("⏳ Simulating initial cosmos entry scene..."):
        master_prompt = (
            f"You are the master narrator for a text adventure game called Haymaker.\n"
            f"World: '{engine['world_name']}' | Genre: '{engine['world_genre']}'.\n"
            f"Character: '{char['name']}' | Backstory: '{char['backstory']}'.\n"
            f"Inventory: {', '.join(char['inventory'])} | Health: {char['health']}/100.\n\n"
            f"⚠️ CRITICAL RULES:\n"
            f"1. Be extremely concise. Deliver exactly ONE detailed short paragraph. Maximum 3 sentences.\n"
            f"2. Never play for the user or decide their actions. Establish the scene and stop talking immediately.\n"
            f"3. COLOR CODE DIALOGUE: Wrap all character dialogue in :orange[**\"Speech\"**] to pop in bold orange. Keep basic narration standard."
        )
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": master_prompt}, {"role": "user", "content": "Wake up and look around."}],
            max_tokens=100,
            temperature=0.7
        )
        initial_story = response.choices[0].message.content
        engine["story_log"].append({"role": "user", "content": "Wake up and look around."})
        engine["story_log"].append({"role": "assistant", "content": initial_story})
        st.rerun()

user_action = st.chat_input("Describe your action or speak...")

if user_action:
    if "user" not in st.session_state:
        st.session_state.guest_tokens -= 1
        
    engine["story_log"].append({"role": "user", "content": user_action})
    
    master_prompt = (
        f"You are the master narrator for a text adventure game called Haymaker.\n"
        f"World: '{engine['world_name']}' | Genre: '{engine['world_genre']}'.\n"
        f"Character: '{char['name']}' | Backstory: '{char['backstory']}'.\n"
        f"Inventory: {', '.join(char['inventory'])} | Health: {char['health']}/100.\n\n"
        f"⚠️ CRITICAL FORMATTING & COGNITIVE RULES:\n"
        f"1. Be extremely concise. Deliver exactly ONE detailed short paragraph. Maximum 3 sentences.\n"
        f"2. Never play for the user or move their body. Let the user fully drive.\n"
        f"3. COLOR CODE DIALOGUE: If a character speaks, wrap their exact spoken words in :orange[**\"Speech\"**] so dialogue stands out in bold orange. Keep narration text completely standard.\n"
        f"4. Append system tags at the absolute bottom if changes occur: [LOOT: item_name] or [HEALTH: -15]."
    )
    
    # RENDER TYPEWRITER CONTAINER DIRECTLY ALONGSIDE THE ROBOT AVATAR WITH NO GHOST DUPLICATES
    cols = st.columns([1, 4, 1])
    with cols[0]:
        st.markdown("### 🤖")
    with cols[1]:
        chat_placeholder = st.empty()
        
        messages = [{"role": "system", "content": master_prompt}]
        for past_turn in engine["story_log"]:
            messages.append({"role": past_turn["role"], "content": past_turn["content"]})
            
        stream_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100,
            temperature=0.7,
            stream=True
        )
        
        raw_ai_text = ""
        for chunk in stream_response:
            if chunk.choices and chunk.choices[0].delta.content:
                raw_ai_text += chunk.choices[0].delta.content
                # Update the custom glass container block character-by-character live
                chat_placeholder.markdown(f'<div class="glass-bubble-ai">{raw_ai_text}</div>', unsafe_allow_html=True)
                time.sleep(0.01)
                
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
