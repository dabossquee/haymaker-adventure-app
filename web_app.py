import streamlit as st
import os
import re
import time
import stripe
import requests
import replicate  # 🚀 CHOSEN ENGINE: Loads the fast, indie-hacker approved image creation tool
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. CORE ENGINE PAGE INITIALIZATION (MUST STAY AT THE TOP)
st.set_page_config(page_title="Haymaker Hub", page_icon="🪐", layout="wide")

# 🌐 THE MASTER HAYMAKER TRANSLATION DICTIONARY MAP
LOCALIZATION_VAULT = {
    "English": {
        "welcome": "### ⚔️ UNLEASH YOUR UNIVERSE",
        "tagline": "To grinders, daydreamers, and creators: You work hard. Now it's time to play hard.",
        "btn_premium": "🚀 ACTIVATE PREMIUM PASS — $10 / WEEK",
        "btn_verify": "🔄 Verify Payment Token Status",
        "tab_create": "🌌 Universe Creator",
        "tab_adventure": "⚔️ Adventure Engine",
        "tab_avatars": "🎭 Identity Portal",
        "tab_profile": "🔑 Account Profile",
        "status_control": "📡 STATUS CONTROL"
    },
    "Español (Spanish)": {
        "welcome": "### ⚔️ DESATA TU UNIVERSO",
        "tagline": "Para los que trabajan duro, los soñadores y los creadores: Trabajas duro. Ahora es el momento de jugar duro.",
        "btn_premium": "🚀 ACTIVAR PASE PREMIUM — $10 / SEMANA",
        "btn_verify": "🔄 Verificar Estado del Token de Pago",
        "tab_create": "🌌 Creador de Universos",
        "tab_adventure": "⚔️ Motor de Aventura",
        "tab_avatars": "🎭 Portal de Identidad",
        "tab_profile": "🔑 Perfil de Cuenta",
        "status_control": "📡 CONTROL DE ESTADO"
    },
    "简体中文 (Mandarin)": {
        "welcome": "### ⚔️ 解放你的宇宙",
        "tagline": "献给苦干者、白日梦想家和创作者：你工作努力。现在是尽情玩耍的时候了。",
        "btn_premium": "🚀 激活尊享通行证 — $10 / 周",
        "btn_verify": "🔄 验证支付代币状态",
        "tab_create": "🌌 宇宙创作者",
        "tab_adventure": "⚔️ 冒险引擎",
        "tab_avatars": "🎭 身份门户",
        "tab_profile": "🔑 账户个人资料",
        "status_control": "📡 状态控制"
    }
}

# 🌐 GLOBAL LOCALIZATION STATE RUNWAY INITIALIZATION
if "app_language" not in st.session_state:
    st.session_state["app_language"] = None

# 📡 SYSTEM CORES INITIALIZATION: Anchor default states before any layout elements render
if "world_cover_url" not in st.session_state:
    st.session_state["world_cover_url"] = "https://picsum.photos"

if "guest_tokens" not in st.session_state:
    st.session_state["guest_tokens"] = 12  # Standard trial buffer fallback safety state

# 🎵 LOCAL CUSTOM AUDIOSCAPE STORAGE INITIALIZATION
if "audio_state" not in st.session_state:
    st.session_state.audio_state = {
        "playing": True, 
        "track_url": "assets/menu_theme.mp3"  # Points to your fresh custom campaign file!
    }

# ---------------------------------------------------------
# 🌐 THE ENTERPRISE LOCALIZATION CHECKPOINT GATEWAY (FRONT GATE)
# ---------------------------------------------------------
if st.session_state.get("app_language") is None:
    st.markdown("# ⚔️ HAYMAKER INDUSTRY")
    st.markdown("### 🪐 Select Your Structural Language Matrix / Seleccione Su Idioma / 请选择您的语言")
    st.write("Establish your dynamic profile localization interface parameters before entering the sandbox workspace.")
    
    selected_matrix_lang = st.selectbox(
        "🌐 Choose Interface Language Node:",
        ["English", "Español (Spanish)", "简体中文 (Mandarin)"],
        key="sb_global_onboarding_language_picker"
    )
    
    if st.button("🚀 IGNITE APPLICATION INTERFACE", use_container_width=True):
        st.session_state.app_language = selected_matrix_lang
        
        # 👑 SECURE PROFILE SYNC: Save choice if authenticated
        if "user" in st.session_state:
            try:
                if "access_token" in st.session_state:
                    supabase_client.postgrest.auth(st.session_state["access_token"])
                supabase_client.table("profiles").upsert({
                    "id": st.session_state.user.id,
                    "interface_language": str(selected_matrix_lang)
                }).execute()
            except Exception:
                pass
                
        st.success(f"⚡ Interface matrix locked to {selected_matrix_lang}! Syncing layout scales...")
        time.sleep(1.0)
        st.rerun()
        
    st.stop() # 🛑 ABSOLUTE EMERGENCY BREAK: Freezes the layout completely right here so sidebars/tabs stay hidden!


# GLOBAL THEME DESIGN: High-Contrast Modern Tech Dynamic UI Skin
st.markdown("""
<style>
    .stApp {
        background-color: #05030a !important;
        background-image: none !important;
        color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #cbd5e1 0%, #a2adb9 50%, #788596 100%) !important;
        border-right: 2px solid #2e1566 !important;
        box-shadow: inset -4px 0px 12px rgba(0,0,0,0.25), 4px 0px 20px rgba(0,0,0,0.4) !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label {
        color: #0f172a !important; font-weight: 700 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 14px; background-color: #020005 !important; padding: 10px;
        border-radius: 24px; border: 1px solid #1e1538; box-shadow: inset 0 4px 12px rgba(0,0,0,0.6);
    }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(180deg, #cbd5e1 0%, #cbd5e1 100%) !important;
        color: #0f172a !important; font-weight: 700 !important; text-transform: uppercase;
        letter-spacing: 0.8px; font-size: 13px !important; padding: 10px 24px !important;
        border-radius: 20px !important; border-top: 1px solid #ffffff !important;
        border-left: 1px solid #ffffff !important; border-right: 2px solid #64748b !important;
        border-bottom: 3px solid #475569 !important; box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important; margin-bottom: 2px !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4c1d95 0%, #1e1b4b 100%) !important;
        color: #ffffff !important; padding: 14px 28px !important; 
        border-top: 1px solid #7c5dfa !important; border-left: 1px solid #7c5dfa !important;
        border-right: 1px solid #0f172a !important; border-bottom: 1px solid #0f172a !important;
        box-shadow: inset 0px 4px 10px rgba(0,0,0,0.8), 0 0 20px rgba(124, 93, 250, 0.3) !important;
        transform: translateY(2px) !important;
    }
    .premium-discovery-card {
        background: #110c1f !important; border-radius: 20px !important;
        border-top: 1px solid #3b2c63 !important; border-left: 1px solid #3b2c63 !important;
        border-right: 2px solid #05020a !important; border-bottom: 4px solid #05020a !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5) !important; margin-bottom: 24px !important;
        overflow: hidden !important; display: flex !important; flex-direction: column;
    }
    .sidebar-avatar-frame {
        width: 130px; height: 130px; background-color: #161026; border-radius: 40px !important;
        border-top: 2px solid #ffffff; border-left: 2px solid #ffffff;
        border-right: 2px solid #475569; border-bottom: 4px solid #1e293b;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3); margin: 16px auto;
        display: flex; align-items: center; justify-content: center; font-size: 50px;
    }
    .stButton > button {
        background: linear-gradient(180deg, #cbd5e1 0%, #94a3b8 100%) !important;
        color: #0f172a !important; font-weight: 700 !important; text-transform: uppercase;
        letter-spacing: 0.5px; border-radius: 18px !important; border-top: 1px solid #ffffff !important;
        border-left: 1px solid #ffffff !important; border-right: 2px solid #475569 !important;
        border-bottom: 4px solid #334155 !important; box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
    }
    .stButton > button:hover {
        color: #ffffff !important; background: linear-gradient(180deg, #7c5dfa 0%, #5b21b6 100%) !important;
    }
    /* 🌌 IMMERSIVE LIVE CANVAS BACKGROUND OVERLAY MATRIX */
    .immersive-chat-viewport {
        background-position: center !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        border-radius: 24px !important;
        padding: 24px !important;
        border: 1px solid rgba(124, 93, 250, 0.15) !important;
        box-shadow: inset 0 0 100px rgba(0,0,0,0.85), 0 20px 40px rgba(0,0,0,0.6) !important;
        margin-top: 16px !important;
    }
    /* Translucent frosted glass effect to keep reading text crisp and legible over any artwork */
    .glass-frosted-scroller {
        background-color: rgba(5, 3, 10, 0.75) !important;
        backdrop-filter: blur(12px) saturate(160%);
        -webkit-backdrop-filter: blur(12px) saturate(160%);
        border-radius: 20px !important;
        padding: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_SECRET = os.getenv("STRIPE_SECRET_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")  # 🔒 Loaded safely into server memory


if not API_KEY or not SUPABASE_URL or not SUPABASE_KEY:
    st.error("🔒 Missing crucial core environment variables inside your hidden .env file!")
    st.stop()

openai_client = OpenAI(api_key=API_KEY)
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if STRIPE_SECRET:
    stripe.api_key = STRIPE_SECRET

# POP-UP MODAL WINDOW GATEWAY
if "active_modal" in st.session_state and st.session_state.active_modal:
    modal = st.session_state.active_modal
    @st.dialog(modal["title"])
    def render_modal_window():
        st.image(modal["img"], use_container_width=True)
        st.markdown(f"**🎨 Creator ID Token:** `{modal['creator']}`")
        st.markdown(f"**🎭 Character Dossier Summary:** {modal['bio']}")
        if st.button("🚪 Close Dossier File", use_container_width=True):
            st.session_state.active_modal = None
            st.rerun()
    render_modal_window()

# STRIPE SUITE CHECKS
if "success" in st.query_params and st.query_params["success"] == "true":
    st.session_state.is_premium = True
    st.toast("👑 Premium Unlimited Pass Activated Successfully!")

# TRIAL VARIABLES STORAGE INITIALIZATION
if "user" not in st.session_state:
    if "guest_tokens" not in st.session_state:
        st.session_state.guest_tokens = 12  
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
# 5. DYNAMIC SIDEBAR OVERWATCH PANEL
with st.sidebar:
    st.title("STATUS CONTROL")
    st.divider()
    
    # 🚪 HOME TERMINAL ESCAPE GATEWAY
    if engine["world_name"]:
        if st.button("🚪 ABANDON TIMELINE (HOME HUB)", type="secondary", key="sidebar_exit_timeline_gate", use_container_width=True):
            st.session_state.world_engine = {
                "world_id": None, "world_name": "", "world_genre": "",
                "player_character": {"name": "", "backstory": "", "health": 100, "inventory": ["survival gear"]},
                "story_log": []
            }
            if "world_cover_url" in st.session_state:
                st.session_state.world_cover_url = "https://picsum.photos"
            st.rerun()
        st.divider()
        


  
    # 🔐 PHASE 1 PROTOCOL: The Ironclad Paywall Vault Execution Checks
    if "user" in st.session_state:
        user_id = st.session_state.user.id
        
               # 📡 LIVE VAULT INVENTORY: Verify subscription metadata & language records directly from your database
        try:
            # 🌐 STEP 3 ARCHITECTURE: Select BOTH columns to load their saved language matrix
            profile_query = supabase_client.table("profiles").select("is_premium, interface_language").eq("id", user_id).single().execute()
            
            if profile_query.data:
                is_premium = profile_query.data.get("is_premium", False)
                saved_lang = profile_query.data.get("interface_language")
                
                # 🪐 AUTOMATED PROFILE LOADING: Instantly lock in their saved language choice if it exists
                if saved_lang:
                    st.session_state.app_language = saved_lang
            else:
                is_premium = False
        except Exception:
            is_premium = False  # Strict default safety gate fallback position


        # 👑 THE PAYWALL GATEWAY: Halt non-paying accounts instantly before loading any story engines
        if not is_premium:
            st.markdown("### ⚔️ UNLEASH YOUR UNIVERSE")
            st.write(
                "To grinders, daydreamers, and creators: You work hard. Now it's time to play hard. "
                "Corporate apps censor your imagination—this is your unfiltered independent sanctuary. "
                "Unlock infinite text-adventure worlds, custom storylines, and atmospheric soundtracks instantly."
            )
            
            st.info("💡 Pro Tip: Complete your character and world architecture customization framework in the options tab first to lock in your timeline blueprint before activating access.")
            
            # 💳 STRIPE INTEGRATION PAYLOAD: Replace with your actual live Stripe Payment Link URL string
            stripe_checkout_url = "https://stripe.com" 
            
            st.markdown(
                f'<a href="{stripe_checkout_url}" target="_blank" style="text-decoration: none;">'
                '<div style="background-color: #00FF66; color: black; text-align: center; padding: 14px; '
                'font-weight: bold; border-radius: 6px; font-size: 18px; margin-top: 15px; margin-bottom: 25px;">'
                '🚀 ACTIVATE PREMIUM PASS — $10 / WEEK</div></a>',
                unsafe_allowed_html=True
            )
            
            st.warning("⚠️ Access Pending: Once your Stripe transaction processes cleanly, click the refresh button below to verify your token state and unlock your sandbox canvas panel.")
            if st.button("🔄 Verify Payment Token Status"):
                st.rerun()
                
            st.stop() # ABSOLUTE EMERGENCY BREAK: Freezes the entire file from compiling further for this session

        # 🟢 ACCESS GRANTED: Paid subscribers pass cleanly past the gate
        st.success(f"👑 PREMIUM PILOT AUTHENTICATED: {st.session_state.user.email}")
        
    else:
        if st.session_state.guest_tokens > 0:
            st.warning(f"⏳ TRIAL ACTIVE: {st.session_state.guest_tokens} Actions Left")
        else:
            st.error("🔒 Action Pool Depleted!")
            
    st.divider()

    
    # HOUSING FRAME FOR PLAYER PROFILE IMAGE
    avatar_display = "👤" if not engine["world_name"] else "🎭"
    st.markdown(f'<div class="sidebar-avatar-frame">{avatar_display}</div>', unsafe_allow_html=True)
    
    # USERNAME DISPLAY TRACKER
    display_username = char["name"] if char["name"] else "Wanderer"
    st.markdown(f"<p style='text-align: center; font-size: 16px; margin: 0;'>Dreamer: <span style='font-weight: 800; color: #4c1d95;'>{display_username}</span></p>", unsafe_allow_html=True)
    
    st.divider()

    
       # 🎵 DYNAMIC SYSTEM AUDIO MATRICES DECK
    with st.expander("🎵 AMBIENT AUDIOSCAPE", expanded=True):
        if not engine["world_name"]:
            st.markdown("<p style='text-align: center; font-size: 13px; color: #334155; font-weight: bold; margin: 5px 0;'>✨ To listen to music, join or forge a world timeline</p>", unsafe_allow_html=True)
        else:
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                if st.session_state.audio_state["playing"]:
                    if st.button("🔇 Mute Audio", use_container_width=True, key="btn_mute_audio_chan"):
                        st.session_state.audio_state["playing"] = False
                        st.rerun()
                else:
                    if st.button("🔊 Play Audio", use_container_width=True, key="btn_play_audio_chan"):
                        st.session_state.audio_state["playing"] = True
                        st.rerun()
                        
            with col_m2:
                if st.button("🔀 Next Track", use_container_width=True, key="btn_next_audio_track"):
                    # Define our master 11-track general post-rock campaign playlist map array
                    playlist_deck = [
                        "assets/menu_theme.mp3",
                        "assets/adventure_loop.mp3",
                        "assets/track_1.mp3", "assets/track_2.mp3", 
                        "assets/track_3.mp3", "assets/track_4.mp3",
                        "assets/track_5.mp3", "assets/track_6.mp3",
                        "assets/track_7.mp3", "assets/track_8.mp3"
                    ]
                    
                    current_track = st.session_state.audio_state["track_url"]
                    try:
                        current_index = playlist_deck.index(current_track)
                        next_index = (current_index + 1) % len(playlist_deck)
                    except ValueError:
                        next_index = 0
                    
                    chosen_track = playlist_deck[next_index]
                    if os.path.exists(chosen_track):
                        st.session_state.audio_state["track_url"] = chosen_track
                    else:
                        st.session_state.audio_state["track_url"] = "assets/menu_theme.mp3"
                        
                    st.session_state.audio_state["playing"] = True
                    st.rerun()
                    
            if st.session_state.audio_state["playing"]:
                st.audio(st.session_state.audio_state['track_url'], format="audio/mp3", loop=True)
                st.caption("🔊 Click play on the official deck to authorize stream")
            else:
                st.markdown("<p style='font-size: 11px; text-align: center; color: #7f1d1d; margin: 10px 0 0 0; font-weight: bold;'>⚠️ System Audio Channel Disabled 🔴</p>", unsafe_allow_html=True)

    
    # SIDEBAR LOGIN & LOGOUT TOGGLE CONTROLS
    if "user" in st.session_state:
        if st.button("🚪 LOG OUT ACCOUNT", type="primary", key="sidebar_logout_gate", use_container_width=True):
            supabase_client.auth.sign_out()
            st.session_state.clear()
            st.rerun()
    else:
        st.info("💡 Want unlimited actions?")
        if st.button("🔑 SIGN IN / SIGN UP", key="sidebar_auth_gateway_redirect", use_container_width=True):
            st.toast("⚡ Head over to your 'Account Profile' hub tab right on the main panel to log in or register instantly.")
    st.divider()

    # ⚙️ SYSTEM SETTINGS & SUBSCRIPTION MANAGEMENT OVERWATCH
    with st.expander("⚙️ SETTINGS CONTROL", expanded=False):
        st.caption("🔒 Sandbox Platform Account Verified")
        st.subheader("💳 Subscription Status")
        
        if getattr(st.session_state, 'is_premium', False):
            st.success("👑 STATUS: Premium Pass Active")
            st.caption("Your timeline capabilities are fully un-capped.")
        else:
            st.warning("⏳ STATUS: Free Trial Mode (12 Actions)")
            
        st.divider()
        st.markdown("#### 📡 Re-Sync Past Purchases")
        st.caption("Changed phones or reinstalled? Tap below to scan Stripe for your active billing cycle account profiles.")
        
        # 🔄 DYNAMIC REACTIVE SUB RECOVERY MATRIX
        if st.button("🔄 Sync & Restore Subscription", key="btn_reactive_sync_stripe_gate", use_container_width=True):
            if "user" not in st.session_state:
                st.error("🔒 Please sign in via the 'Account Profile' tab first so we can map your purchase history securely!")
            else:
                with st.spinner("⏳ Scanning Stripe secure merchant databases for active account tokens..."):
                    try:
                        import stripe
                        if STRIPE_SECRET:
                            stripe.api_key = STRIPE_SECRET
                        else:
                            stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
                            
                        user_email = st.session_state.user.email
                        customers = stripe.Customer.list(email=user_email, limit=1)
                        
                        if customers.data:
                            customer = customers.data[0]
                            subs = stripe.Subscription.list(customer=customer.id, status="active", limit=1)
                            trial_subs = stripe.Subscription.list(customer=customer.id, status="trialing", limit=1)
                            
                            if subs.data or trial_subs.data:
                                st.session_state.is_premium = True
                                st.toast("👑 Premium Subscription Successfully Restored! Welcome back, Pilot.")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ No active paid billing accounts found matching this email on the Stripe ledger.")
                        else:
                            st.error("❌ No verified customer account files exist for this email address yet.")
                    except Exception as stripe_api_err:
                        st.error(f"Sync Fault: {stripe_api_err}")
                        st.caption("Ensure your STRIPE_SECRET_KEY is fully written inside your hidden .env file container.")
                        
        st.divider()
        st.markdown("<p style='font-size: 11px; color: #475569; font-style: italic; text-align: center;'>Haymaker Industry Security Architecture v1.02 • Privacy Framework Protected</p>", unsafe_allow_html=True)

# 6. BALA DISCOVERY CORE ARCHITECTURE
if not engine["world_name"]:
    st.title("🪐 Haymaker Industry Hub")
    st.subheader("Explore alternate realities or forge your own timeline")
    
    # Core main navigation elements defined cleanly inside the home block scope
    tab_explore, tab_my_creations, tab_create, tab_avatars, tab_profile = st.tabs([
        "Explore Universes", "My Creations", "Create a World", "Community Avatars", "Account Profile"
    ])
    
    with tab_explore:
        # Multi-genre discovery selection tabs initialized directly within the explore scope
        sub_ai, sub_cyberpunk, sub_fantasy, sub_horror, sub_romance, sub_scifi = st.tabs([
            "Community & AI", "Cyberpunk", "Dark Fantasy", "Horror", "Romance", "Sci-Fi"
        ])
        
        with sub_ai:
            st.markdown("### Public Community Timelines")
            try:
                public_worlds = supabase_client.table("worlds").select("*").order("created_at", desc=True).execute()
                if public_worlds.data:
                    cols_ai = st.columns(2)
                    for index, world_row in enumerate(public_worlds.data):
                        with cols_ai[index % 2]:
                            st.markdown(f"""
                            <div class="premium-discovery-card">
                                <div style="padding:20px;">
                                    <h4>🪐 {world_row['world_name'].upper()}</h4>
                                    <p style='color: #a78bfa; font-size: 12px; font-weight: bold;'>THEMATIC GENRE: {world_row['world_genre'].upper()}</p>
                                    <p style='color: #94a3b8; font-size: 14px;'>A custom alternate timeline forged by an active player sandbox node.</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button("🎮 Enter Community Universe", key=f"pub_{world_row['id']}_{index}", use_container_width=True):
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
                
        with sub_cyberpunk:
            st.markdown("### Curated Cyberpunk Realities")
            cyber_presets = [
                {"id": "c1", "name": "Neo-Tokyo Runner", "bio": "High-stakes tech espionage, corporate warfare, and neon-lit street racing.", "char": "Ren Tanaka", "story": "A street racer with a corporate data package hardwired into his skull."},
                {"id": "c2", "name": "Gridlock Underground", "bio": "Hack deep mainframe grids and lead a digital rebellion against mega-corps.", "char": "Echo", "story": "A phantom hacker who lives inside deep mainframe server nodes."}
            ]
            cols_cyber = st.columns(2)
            for index, p in enumerate(cyber_presets):
                with cols_cyber[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>🏙️ {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_cyber_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Cyberpunk"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()

        with sub_fantasy:
            st.markdown("### Curated Dark Fantasy Realities")
            fantasy_presets = [
                {"id": "f1", "name": "Vampire Nomad", "bio": "Navigate exile, bloodlines, and dark covens in a gothic world of endless night.", "char": "Kaelen Voss", "story": "An ancient rogue vampire cast out of the High Court, hunting bounty squads."},
                {"id": "f2", "name": "Ashelands Renegade", "bio": "A tactical swords-and-sorcery survival gauntlet across a ruined kingdom.", "char": "Gideon Black", "story": "A weathered mercenary carrying a broken crown across fields of ash."}
            ]
            cols_fant = st.columns(2)
            for index, p in enumerate(fantasy_presets):
                with cols_fant[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>🧙 {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_fant_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Dark Fantasy"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()
        with sub_horror:
            st.markdown("### Curated Horror Realities")
            horror_presets = [
                {"id": "h1", "name": "Asylum Phantoms", "bio": "Escape an abandoned psychiatric hospital while tracking sanity meters.", "char": "Arthur Vance", "story": "An investigative journalist locked inside an asylum wing with moving shadows."},
                {"id": "h2", "name": "Cabin Isolation", "bio": "Survive a night in a remote woodland estate stalked by masked cultists.", "char": "Sarah", "story": "A standard hiker forced to fortify a hunting cabin before midnight strikes."}
            ]
            cols_horror = st.columns(2)
            for index, p in enumerate(horror_presets):
                with cols_horror[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>🩸 {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_horror_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Horror"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()

        with sub_romance:
            st.markdown("### Curated Romance Realities")
            romance_presets = [
                {"id": "r1", "name": "Neon Heartbeats", "bio": "A high-stakes corporate romance tangled inside a Tokyo cyber espionage ring.", "char": "Leo Cruz", "story": "A security auditor falling for the rival terminal hacker assigned to clear his deck."},
                {"id": "r2", "name": "Starlight Station", "bio": "Find love and connection at the absolute edge of an expanding galaxy.", "char": "Elena", "story": "A deep-space botanist stationed on a lonely supply node with a rogue freighter captain."}
            ]
            cols_romance = st.columns(2)
            for index, p in enumerate(romance_presets):
                with cols_romance[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>❤️ {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_rom_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Romance"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()

        with sub_scifi:
            st.markdown("### Curated Sci-Fi Realities")
            scifi_presets = [
                {"id": "s1", "name": "Sector 7 Nomad", "bio": "Grit, survival, and starship dogfights across an outlaw solar system.", "char": "Pilot Vance", "story": "A disgraced military pilot running illicit scrap metal through asteroid fields."},
                {"id": "s2", "name": "Chronos Station", "bio": "A psychological thriller aboard a deep-space station stuck in a time anomaly.", "char": "Dr. Aris", "story": "The chief technician investigating a quantum pulse that locked the terminal clock."}
            ]
            cols_scifi = st.columns(2)
            for index, p in enumerate(scifi_presets):
                with cols_scifi[index % 2]:
                    st.markdown(f"""
                    <div class="premium-discovery-card">
                        <div style="padding:20px;">
                            <h4>🚀 {p['name'].upper()}</h4>
                            <p style='color: #94a3b8; font-size: 14px;'>{p['bio']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Launch Scenario", key=f"btn_{p['id']}", use_container_width=True):
                        engine["world_id"] = f"pre_scifi_{p['id']}"
                        engine["world_name"] = p["name"]
                        engine["world_genre"] = "Sci-Fi"
                        char["name"] = p["char"]
                        char["backstory"] = p["story"]
                        st.rerun()
    with tab_my_creations:
        st.markdown("### Your Private Universes")
        if "user" in st.session_state:
            try:
                my_worlds = supabase_client.table("worlds").select("*").eq("creator_id", st.session_state.user.id).order("created_at", desc=True).execute()
                if my_worlds.data:
                    for index, my_row in enumerate(my_worlds.data):
                        st.markdown(f"""
                        <div class="premium-discovery-card">
                            <div style="padding:20px;">
                                <h4>🪐 {my_row['world_name'].upper()}</h4>
                                <p style='color: #a78bfa; font-size: 13px; font-weight: bold;'>THEMATIC GENRE: {my_row['world_genre'].upper()}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        cols_actions = st.columns(2)
                        with cols_actions[0]:
                            if st.button("🎮 Resume Timeline", key=f"resume_{my_row['id']}_{index}", use_container_width=True):
                                engine["world_id"] = my_row["id"]
                                engine["world_name"] = my_row["world_name"]
                                engine["world_genre"] = my_row["world_genre"]
                                char["name"] = "Unknown Wanderer"
                                char["backstory"] = "A traveler stepping directly back into their verified alternate reality timeline checkpoint."
                                st.rerun()
                        with cols_actions[1]:
                            if st.button("🗑️ Delete World", key=f"purge_{my_row['id']}_{index}", type="primary", use_container_width=True):
                                try:
                                    # 👑 THE RLS CLEARANCE FIX: Explicitly inject the user's active session token into the network headers
                                    if "access_token" in st.session_state:
                                        supabase_client.postgrest.auth(st.session_state["access_token"])
                                    
                                    # Execute the authenticated delete statement on your live database rows
                                    supabase_client.table("worlds").delete().eq("id", my_row["id"]).eq("creator_id", st.session_state.user.id).execute()
                                    st.toast("💥 Timeline completely erased from the local vault and public community servers!")
                                    st.rerun()
                                except Exception as err:
                                    st.error(f"Purge Fault: {err}")

                        st.divider()
                else:
                    st.info("You haven't deployed any permanent universes yet. Forge one inside the 'Create a World' tab!")
            except Exception as e:
                st.error(f"Vault Connection Error: {e}")
        else:
            st.warning("🔒 Please sign in via the 'Account Profile' tab to look inside your private creation vault.")

    with tab_create:
        # 🌌 PHASE 0: DEEP WORLD CUSTOMIZATION ARCHITECT
        st.markdown("### ⚔️ Universe Architect Form")
        st.write("Tune the fundamental mechanics of your custom timeline before initializing the narrative seed.")

        # Layout Column Splitting for Clean UI Design Matrix
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("##### 🪐 Celestial Physics")
            w_name = st.text_input("Universe Name:", placeholder="e.g., Sector 7, Neo-Tokyo")
            w_genre = st.selectbox("Select thematic genre:", ["Sci-Fi", "Dark Fantasy", "Cyberpunk", "Horror", "Romance", "Other"])
            
            # Gravity and Atmospheric sliders to hook ADHD hyper-focus instantly
            world_gravity = st.slider("🪐 Gravity Levels", min_value=0.1, max_value=5.0, value=1.0, step=0.1, 
                                      help="1.0 is standard Earth baseline gravity. Affects combat logistics and movement mechanics.")
            world_atmosphere = st.select_slider("💨 Atmospheric Density", 
                                                options=["Vacuum (Space)", "Thin / Toxic", "Breathable Baseline", "Hyper-Dense / Corrosive"],
                                                value="Breathable Baseline")

        with col_right:
            st.markdown("##### 🎭 Character Identity Settings")
            c_name = st.text_input("Your character's name:")
            c_backstory = st.text_area("Character profile/backstory:")

        st.markdown("##### 🦅 Faction Architecture & Frictional Elements")
        faction_allies = st.text_input("🦅 Dominant / Allied Faction Name", placeholder="e.g., Vanguard Coalition, Iron Syndicate")
        faction_enemies = st.text_input("💀 Rogue / Opposing Faction Name", placeholder="e.g., Sector Insurgency, Waste Marauders")
        
        # Open canvas text block for deep world lore dumping
        world_custom_lore = st.text_area("✍️ Custom Environmental Directives / Constraints", 
                                         placeholder="Inject specific universe rules here... (e.g., 'The air is highly combustible, energy shields are banned, or characters look like Master Chief armor variants')",
                                         height=80)
        
        st.divider()

        if st.button("🚀 Deploy and Ignite Core Engine", use_container_width=True):
            if w_name and w_genre and c_name and faction_allies and faction_enemies:
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
                
                # 👑 THE ADVANCED PROTOCOL PACKAGING: Bundle the sliders into memory state matrices
                engine["world_name"] = w_name
                engine["world_genre"] = w_genre
                
                # Inject the customized physics and faction parameters right into the backend engine storage dictionary
                engine["world_customization"] = {
                    "gravity": world_gravity,
                    "atmosphere": world_atmosphere,
                    "allies": faction_allies,
                    "enemies": faction_enemies,
                    "lore": world_custom_lore
                }
                
                char["name"] = c_name
                char["backstory"] = c_backstory
                st.success("🎉 Custom universe timeline seed compiled successfully!")
                time.sleep(1.0)
                st.rerun()
            else:
                st.warning("⚠️ Architect Refusal: Fill out all fields, including Factions, to launch the framework.")


    with tab_avatars:
        st.markdown("### Community Avatars Portal")
        st.caption("Browse live identities forged across active world timelines.")
        st.divider()
        
        # 🎨 THE SECURE AVATAR FORGE SANDBOX ENTRY ZONE
        st.markdown("#### Select Your Identity Portrait")
        st.write("Select a curated high-end cinematic profile character avatar card to sync to your identity vault profile.")
        
        is_user_premium = getattr(st.session_state, 'is_premium', False)
        ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
        
        # 👑 Secure Boss Mode Authorization Check
        if "user" in st.session_state and ADMIN_EMAIL:
            if st.session_state.user.email == ADMIN_EMAIL:
                is_user_premium = True

        # 👥 CURATED STATIC VAULT IMAGES: High-end pre-made visual assets to prevent connection hanging
        avatar_options = {
            "🥷 Cybernetic Shinobi / Tactical Operator": "https://picsum.photos",
            "🧙‍♂️ Arcane Runemaster / Dark Sorcerer": "https://picsum.photos",
            "🚀 Dreadnought Pilot / Space Marine": "https://picsum.photos",
            "💀 Wasteland Scavenger / Nomad Raider": "https://picsum.photos"
        }
        
        selected_avatar_name = st.selectbox("Choose your visual identity archetype:", list(avatar_options.keys()), key="sb_avatar_archetype_choice")
        chosen_public_url = avatar_options[selected_avatar_name]
        
        # Display a quick visual preview layout box of their active choice
        st.image(chosen_public_url, caption=f"Selected Blueprint: {selected_avatar_name}", width=200)
        
        if st.button("✨ Lock Identity Profile", use_container_width=True, key="btn_forge_avatar_sandbox_trigger"):
            if "user" not in st.session_state:
                st.error("🔒 Access Locked: Please create an account or sign in via the Account Profile tab to authorize identity protocols.")
            elif not is_user_premium:
                st.error("🔒 Premium Pass Required: Swapping identity profile cards requires an active Avatar, Spartan, or STEM pass tier.")
            else:
                with st.spinner("⏳ Linking high-res asset card to your encrypted vault profile records..."):
                    try:
                        if "access_token" in st.session_state:
                            supabase_client.postgrest.auth(st.session_state["access_token"])
                        
                        # 👑 SECURE DATA SYNC: Lock the clean pre-made link address straight into your profile record columns
                        email_handle = str(st.session_state.user.email).split("@")[0]
                        supabase_client.table("profiles").upsert({
                            "id": st.session_state.user.id,
                            "avatar_url": str(chosen_public_url),
                            "username": str(email_handle),
                            "is_premium": True
                        }).execute()
                        
                        st.success("🎉 Archetype profile asset successfully locked to your permanent encrypted vault!")
                        time.sleep(1.0)
                        st.rerun()
                        
                    except Exception as profile_sync_err:
                        st.error(f"Vault Sync Fault: {profile_sync_err}")
                        
        st.divider()
        st.markdown("#### Active Community Records")

        # 🔒 ISOLATION FIELD: Only attempt to pull records if a verified user session is actively present
        if "user" in st.session_state:
            try:
                profile_records = supabase_client.table("profiles").select("*").execute()
                
                if profile_records.data:
                    # 🎯 THE REAL FIXED UNWRAP: Extract your live data row by checking strings cleanly
                    my_card = None
                    for row in profile_records.data:
                        if str(row.get("id")) == str(st.session_state.user.id):
                            my_card = row
                            break
                    
                    if my_card and my_card.get("avatar_url"):
                        st.markdown("##### 👑 YOUR ACTIVE FORGED IDENTITY")
                        col_me_img, col_me_txt = st.columns(2)
                        with col_me_img:
                            avatar_link = my_card.get("avatar_url")
                            if avatar_link and str(avatar_link) != "None" and "http" in str(avatar_link):
                                st.image(str(avatar_link), use_container_width=True)
                            else:
                                st.image("https://picsum.photos", caption="Matrix Vault Initializing...", use_container_width=True)
                        with col_me_txt:
                            display_name = my_card.get("username", "Wanderer")
                            st.markdown(f"### {str(display_name).upper()}")
                            st.markdown("❤️ **HP:** `100/100` | 🎒 `Active Loadout Secured`")
                            st.caption(f"*Secure Master Signature: user_{my_card.get('id')[:8]}*")
                        st.divider()
                    
                    # Package and build dynamic 3-column layout boxes for all entries in the system ledger
                    valid_community_cards = [row for row in profile_records.data if row.get("avatar_url")]
                    
                    if valid_community_cards:
                        st.markdown("##### 👥 ALLIED TIMELINE DREAMERS")
                        cols = st.columns(3)
                        for idx, card in enumerate(valid_community_cards):
                            col_target = cols[idx % 3]
                            with col_target:
                                st.markdown(f"##### 🎭 {str(card.get('username', 'Wanderer')).upper()}")
                                
                                # 🎯 PUBLIC LOOP FIX: Wrap community image urls in safety checks to block blank fields
                                comm_link = card.get("avatar_url")
                                if comm_link and str(comm_link) != "None" and "http" in str(comm_link):
                                    st.image(str(comm_link), use_container_width=True)
                                else:
                                    st.image("https://picsum.photos", caption="Matrix Vault Initializing...", use_container_width=True)
                                    
                                st.caption(f"*Signature: user_{card.get('id')[:6]}*")
                                st.divider()
                    else:
                        st.info("✨ The public ledger is currently empty. Be the first to forge a custom avatar identity asset above!")
                else:
                    st.info("✨ The public ledger is currently empty. Be the first to forge a custom avatar identity asset above!")
            except Exception as db_read_err:
                st.caption(f"Database Sync Standby: {db_read_err}")
        else:
            st.info("🔑 Please sign in via the 'Account Profile' tab to view live character assets and authorize database ledger streams.")

                
    with tab_profile:
        st.markdown("### User Authentication Center")
        if "user" in st.session_state:
            st.success(f"👑 Secure Profile Synchronized: `{st.session_state.user.email}`")
            if st.button("🚪 Log Out of Platform Account", type="primary", key="main_hub_profile_logout_gate", use_container_width=True):
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
                if st.button("🔓 Authenticate Profile", key="main_hub_auth_gateway_click", use_container_width=True):
                    try:
                        session_data = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = session_data.user
                        if hasattr(session_data, 'session') and session_data.session:
                            st.session_state["access_token"] = session_data.session.access_token
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
    st.stop()
# 7. ACTIVE NARRATIVE DISPLAY CANVAS (COHESIVE iOS FLEX WRAPPERS)
st.markdown("""
<style>
    .chat-row-user { display: flex; justify-content: flex-end; align-items: flex-start; margin: 10px 0px; gap: 10px; }
    .chat-row-ai { display: flex; justify-content: flex-start; align-items: flex-start; margin: 10px 0px; gap: 10px; }
    .avatar-box { font-size: 24px; padding-top: 4px; user-select: none; }
    .glass-bubble-user {
        background-color: rgba(255, 75, 75, 0.18); backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 75, 75, 0.3); border-radius: 16px 16px 2px 16px;
        padding: 12px 16px; color: #ffffff; font-size: 15px; max-width: 70%; text-align: left;
    }
    .glass-bubble-ai {
        background-color: rgba(255, 255, 255, 0.08); backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px 16px 16px 2px;
        padding: 12px 16px; color: #f0f2f6; font-size: 15px; max-width: 70%; text-align: left;
    }
</style>
""", unsafe_allow_html=True)

st.title(f"🎬 {engine['world_name'].upper()}")

is_premium_active = getattr(st.session_state, 'is_premium', False)
has_trial_tokens = st.session_state.guest_tokens > 0

if not is_premium_active and not has_trial_tokens:
    # 👑 THE BULLETPROOF KEY FORCE: Explicitly load the verified key name directly into Stripe
    import stripe
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    # 🔒 LAYER 1 PROTECTION CHECK: If the user is NOT logged in, force the Account Creation Gate first
    if "user" not in st.session_state:
        st.title("🔒 SECURE YOUR CORRIDOR")
        st.subheader("Your 12 free trial action points have been fully exhausted.")
        st.markdown("<p style='color: #a78bfa; font-size: 14px; font-weight: bold;'>To protect your custom timelines, save your progress, and unlock premium navigation passes, you must create a verified account profile first.</p>", unsafe_allow_html=True)
        st.divider()
        
        # In-line high-conversion authentication hub
        auth_mode = st.radio("Choose Action:", ["✨ Create An Account (Sign Up)", "🔑 Access Existing Profile (Log In)"], horizontal=True, key="paywall_gate_auth_toggle")
        
        email_input = st.text_input("📩 Enter Your Email Address:", placeholder="name@example.com", key="input_paywall_auth_email").strip()
        pass_input = st.text_input("🔒 Establish Secure Password (Min. 6 characters):", type="password", placeholder="••••••••", key="input_paywall_auth_password")
        
        if auth_mode == "✨ Create An Account (Sign Up)":
            if st.button("🚀 Forge Encrypted Account Profile", use_container_width=True, type="primary", key="btn_paywall_gate_signup"):
                if email_input and len(pass_input) >= 6:
                    with st.spinner("⏳ Provisioning database matrix vaults..."):
                        try:
                            auth_res = supabase_client.auth.sign_up({"email": email_input, "password": pass_input})
                            if auth_res.user:
                                st.success("🎉 Profile created! An activation link has been sent to your email. Check your inbox and spam folder, then log in right here to unlock the cards!")
                        except Exception as auth_err:
                            st.error(f"Account Creation Fault: {auth_err}")
                else:
                    st.warning("⚠️ Enter a valid email and a password of at least 6 characters to secure your file data.")
                    
        else: # Log In mode
            if st.button("🔑 Authorize Profile Credentials", use_container_width=True, type="primary", key="btn_paywall_gate_login"):
                if email_input and pass_input:
                    with st.spinner("⏳ Verifying profile security signatures..."):
                        try:
                            auth_res = supabase_client.auth.sign_in_with_password({"email": email_input, "password": pass_input})
                            if auth_res.user:
                                st.session_state.user = auth_res.user
                                if auth_res.session and hasattr(auth_res.session, 'access_token'):
                                    st.session_state.access_token = auth_res.session.access_token
                                st.toast("👑 Access Granted! Checking billing authorization profiles...")
                                time.sleep(1)
                                st.rerun()
                        except Exception as auth_err:
                            st.error(f"Authorization Denied: {auth_err}")
                else:
                    st.warning("⚠️ Enter both your registered email and password to pull your account file.")
        
        st.stop() # Stops the page execution right here so they CANNOT see the pricing cards until logged in!

    # 💳 LAYER 2 PROTECTION CHECK: Once they successfully log in, show the checkout cards automatically
    st.title("💳 PLATFORM ACCESS LOCKED")
    st.subheader(f"Welcome back, Pilot ({st.session_state.user.email}). Select a premium navigation pass to unlock the cosmos.")
    st.markdown("<p style='color: #94a3b8; font-size: 14px;'>All tiers are community-priced to be accessible, while fully protecting timeline data streams from heavy asset processing.</p>", unsafe_allow_html=True)
    st.divider()
    
    col_t1, col_t2, col_t3 = st.columns(3)



    
    with col_t1:
        st.markdown("""
        <div style="background: #110c1f; padding: 20px; border-radius: 16px; border: 1px solid #3b2c63; text-align: center; height: 320px;">
            <h3 style="color: #ffffff; margin: 0;">💨 AVATAR PASS</h3>
            <h2 style="color: #7c5dfa; margin: 10px 0;">$4.99<span style="font-size: 14px; color: #94a3b8;"> / wk</span></h2>
            <p style="color: #a78bfa; font-size: 12px; font-weight: bold; margin-bottom: 10px;">📦 ALLOWANCE PROTOCOLS:</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 40,000 Narrative Tokens / wk</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 20 Cinematic Images / wk</p>
            <p style="color: #94a3b8; font-size: 12px; font-style: italic; margin-top: 10px;">Built to be completely affordable for everyday dreamers to escape reality.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Activate Avatar Pass", key="btn_checkout_tier_1", use_container_width=True):
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': 'Haymaker Avatar Pass'},
                            'unit_amount': 499, 'recurring': {'interval': 'week'}
                        },
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url='https://onrender.com',
                    cancel_url='https://onrender.com',
                )
                st.markdown(f"[👉 Click Here to Open Secure Stripe Checkout]({checkout_session.url})")
            except Exception as e:
                st.error(f"Stripe Portal Error: {e}")
                
    with col_t2:
        st.markdown("""
        <div style="background: #161026; padding: 20px; border-radius: 16px; border: 2px solid #7c5dfa; text-align: center; height: 320px; box-shadow: 0 0 15px rgba(124, 93, 250, 0.2);">
            <h3 style="color: #ffffff; margin: 0;">🎖️ SPARTAN PASS</h3>
            <h2 style="color: #a78bfa; margin: 10px 0;">$9.99<span style="font-size: 14px; color: #94a3b8;"> / wk</span></h2>
            <p style="color: #a78bfa; font-size: 12px; font-weight: bold; margin-bottom: 10px;">📦 ALLOWANCE PROTOCOLS:</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 100,000 Narrative Tokens / wk</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 60 Cinematic Images / wk</p>
            <p style="color: #94a3b8; font-size: 12px; font-style: italic; margin-top: 10px;">Our standard premium experience for extended multi-hour sessions.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Activate Spartan Pass", key="btn_checkout_tier_2", type="primary", use_container_width=True):
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': 'Haymaker Spartan Pass'},
                            'unit_amount': 999, 'recurring': {'interval': 'week'}
                        },
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url='https://onrender.com',
                    cancel_url='https://onrender.com',
                )
                st.markdown(f"[👉 Click Here to Open Secure Stripe Checkout]({checkout_session.url})")
            except Exception as e:
                st.error(f"Stripe Portal Error: {e}")
                
    with col_t3:
        st.markdown("""
        <div style="background: #110c1f; padding: 20px; border-radius: 16px; border: 1px solid #3b2c63; text-align: center; height: 320px;">
            <h3 style="color: #ffffff; margin: 0;">🧠 STEM PASS</h3>
            <h2 style="color: #f43f5e; margin: 10px 0;">$19.99<span style="font-size: 14px; color: #94a3b8;"> / wk</span></h2>
            <p style="color: #a78bfa; font-size: 12px; font-weight: bold; margin-bottom: 10px;">📦 ALLOWANCE PROTOCOLS:</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• UNLIMITED Narrative Tokens</p>
            <p style="color: #cbd5e1; font-size: 13px; margin: 2px 0;">• 150 Cinematic Images / wk</p>
            <p style="color: #94a3b8; font-size: 12px; font-style: italic; margin-top: 10px;">Un-capped matrix shield. Built for heavy, continuous 24/7 world roleplay.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Activate STEM Pass", key="btn_checkout_tier_3", use_container_width=True):
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': 'Haymaker STEM Pass'},
                            'unit_amount': 1999, 'recurring': {'interval': 'week'}
                        },
                        'quantity': 1,
                    }],
                    mode='subscription',
                    success_url='https://onrender.com',
                    cancel_url='https://onrender.com',
                )
                st.markdown(f"[👉 Click Here to Open Secure Stripe Checkout]({checkout_session.url})")
            except Exception as e:
                st.error(f"Stripe Portal Error: {e}")
                
    st.stop()

    with st.spinner("⏳ Simulating initial cosmos entry scene & forging visual assets..."):
        try:
            image_prompt = f"Cinematic widescreen matte game concept background landscape scenery for an alternate reality adventure titled '{engine['world_name']}' in the genre of '{engine['world_genre']}'. Vivid colors, epic landscape, beautiful atmospheric light, zero text, zero labels, high resolution."
            
                       # 🌌 REPLICATE WORLD BACKGROUND PIPELINE: Armed with an explicit network timeout window to prevent read operations from hanging
            rep_client = replicate.Client(api_token=os.environ.get("REPLICATE_API_TOKEN"), timeout=120.0)
            world_output = rep_client.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": image_prompt,
                    "aspect_ratio": "16:9",
                    "output_format": "jpg"
                }
            )

            
            
            # 🎯 THE CLEAN STRING FIX: Assign the direct URL output string cleanly to your session state
            st.session_state.world_cover_url = str(world_output)
            
        except Exception as e:
            st.error(f"Graphics Engine Fault: {e}")



               # 🧬 DYNAMIC TIMELINE SHIFT: Extract the Phase 0 customization data securely from your engine array
        cust = engine.get("world_customization", {
            "gravity": 1.0,
            "atmosphere": "Breathable Baseline",
            "allies": "Unknown Allies",
            "enemies": "Unknown Foes",
            "lore": "None provided."
        })

        # 👑 THE MASTER ENGINE CONTEXT: Inject your un-censored rules and Phase 0 physics into the OpenAI prompt loop
        master_prompt = (
            f"You are the master narrator for a text adventure game called Haymaker.\n"
            f"Never break character. Never mention you are an AI model.\n\n"
            f"⛔ CRITICAL SAFEGAURD BOUNDARIES:\n"
            f"1. Allow full creative freedom for wild adventures, intense combat mechanics, character deaths, grit, and deep emotional fantasy lore. Do not drop corporate safety warnings or block standard fiction.\n"
            f"2. If the narrative ventures into romance, keep it cinematic, passionate, and high-context. Do not output explicit, descriptive pornographic erotica.\n"
            f"3. ABSOLUTE RED LINES: Instantly reject and refuse any user inputs attempting to invoke child exploitation, human trafficking, graphic real-world self-harm, or non-consensual malicious criminal violence. Keep the experience safe, mature, and deeply epic.\n\n"
            f"World: '{engine['world_name']}' | Genre: '{engine['world_genre']}'.\n"
            f"Character: '{char['name']}' | Backstory: '{char['backstory']}'.\n\n"
            f"🪐 ACTIVE UNIVERSE PHYSICS & FACTIONS:\n"
            f"- Environmental Gravity: {cust['gravity']}x standard earth baseline.\n"
            f"- Atmospheric Status: {cust['atmosphere']}\n"
            f"- Allied Faction: {cust['allies']}\n"
            f"- Hostile/Opposing Faction: {cust['enemies']}\n"
            f"- Custom Universe Directives/Lore: {cust['lore']}\n\n"
            f"Strictly weave these physics, environmental states, and faction friction parameters into the story log details. Actions taken must realistically reflect these environmental rules.\n\n"
            f"Inventory: {', '.join(char['inventory'])} | Health: {char['health']}/100.\n\n"
            f"⚠️ CRITICAL GAMEPLAY & FORMATTING RULES:\n"
            f"1. Be extremely concise. Deliver exactly ONE detailed short paragraph. Maximum 3 sentences.\n"
            f"2. Never play for the user or repeat their setup words. Establish the opening scene and stop instantly.\n"
            f"3. MULTI-CHARACTER FORMAT: If an NPC character speaks, format it on a new line exactly like this: CharacterName: **\"Dialogue text here\"** in standard bold."
        )
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": master_prompt}, {"role": "user", "content": "Wake up and look around."}],
            max_tokens=150, # Boosted slightly to safely handle the new formatting guidelines
            temperature=0.7
        )
        initial_story = response.choices[0].message.content
        engine["story_log"].append({"role": "user", "content": "Wake up and look around."})
        engine["story_log"].append({"role": "assistant", "content": initial_story})
        st.rerun()


# 9. INJECT DYNAMIC IMMERSIVE VISUAL BACKGROUND WINDOW WRAPPER
    # 🌌 SAFE INITIALIZATION DEPLOYMENT: Safe read with a structural default placeholder fallback path
    bg_url = st.session_state.get("world_cover_url", "https://picsum.photos")
st.markdown(f'<div class="immersive-chat-viewport" style="background-image: url(\'{bg_url}\');">', unsafe_allow_html=True)
st.markdown('<div class="glass-frosted-scroller">', unsafe_allow_html=True)

# Dedicated structural container to force clean chronological rendering order inside the frosted scroller window
chat_canvas_context = st.container()

with chat_canvas_context:
    for text_turn in engine["story_log"]:
        if text_turn["role"] == "user":
            if "[System Command]" in text_turn["content"]:
                st.info(text_turn["content"])
            else:
                st.markdown(f"""
                <div class="chat-row-user">
                    <div class="glass-bubble-user">{text_turn["content"]}</div>
                    <div class="avatar-box">👤</div>
                </div>
                """, unsafe_allow_html=True)
        elif text_turn["role"] == "assistant":
            clean_text = re.sub(r'\[.*?\]', '', text_turn["content"]).strip()
            st.markdown(f"""
            <div class="chat-row-ai">
                <div class="avatar-box">🤖</div>
                <div class="glass-bubble-ai">{clean_text}</div>
            </div>
            """, unsafe_allow_html=True)

user_action = st.chat_input("Describe your action or speak...")

if user_action:
    if "user" not in st.session_state:
        st.session_state.guest_tokens -= 1
        
    engine["story_log"].append({"role": "user", "content": user_action})
    
    with chat_canvas_context:
        st.markdown(f"""
        <div class="chat-row-user">
            <div class="glass-bubble-user">{user_action}</div>
            <div class="avatar-box">👤</div>
        </div>
        """, unsafe_allow_html=True)
    
    master_prompt = (
        f"You are the master narrator for a text adventure game called Haymaker.\n"
        f"World: '{engine['world_name']}' | Genre: '{engine['world_genre']}'.\n"
        f"Character: '{char['name']}' | Backstory: '{char['backstory']}'.\n"
        f"Inventory: {', '.join(char['inventory'])} | Health: {char['health']}/100.\n\n"
        f"⚠️ CRITICAL NARRATOR & DIALOGUE ENFORCEMENT RULES:\n"
        f"1. Be concise. Respond in exactly ONE high-impact paragraph. Maximum 3 sentences total.\n"
        f"2. NEVER repeat the user's input phrase or mirror their exact sentences back to them. Advance the plot immediately.\n"
        f"3. USER ACCESS CONTROLS: The user uses double quotes \" \" to speak in the world. If they talk to someone, you must handle the response for that character.\n"
        f"4. NPC DIALOGUE SEPARATION: Keep your narrator descriptions standard. If an NPC character answers, place it on a clean line formatted exactly like this: CharacterName: <span style='color:#FF4B4B; font-weight:bold;'>\"Dialogue text here\"</span> to isolate dialogue in bold orange-red. Do not use markdown tags like :orange[].\n"
        f"5. Append system data tags at the absolute bottom if changes occur: [LOOT: item_name] or [HEALTH: -15]."
    )
    
    messages = [{"role": "system", "content": master_prompt}]
    for past_turn in engine["story_log"]:
        messages.append({"role": past_turn["role"], "content": past_turn["content"]})
        
    stream_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=120,
        temperature=0.7,
        stream=True
    )
    
    with chat_canvas_context:
        chat_placeholder = st.empty()
        raw_ai_text = ""
        for chunk in stream_response:
            if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                raw_ai_text += chunk.choices[0].delta.content
                chat_placeholder.markdown(f"""
                <div class="chat-row-ai">
                    <div class="avatar-box">🤖</div>
                    <div class="glass-bubble-ai">{raw_ai_text}</div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.04)
                
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

st.markdown('</div></div>', unsafe_allow_html=True)
