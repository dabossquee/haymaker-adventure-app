import streamlit as st
import os
import re
import time
import stripe
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# 1. CORE ENGINE PAGE INITIALIZATION
st.set_page_config(page_title="Haymaker Hub", page_icon="🪐", layout="wide")
# 🎵 LOCAL CUSTOM AUDIOSCAPE STORAGE INITIALIZATION
if "audio_state" not in st.session_state:
    st.session_state.audio_state = {
        "playing": True, 
        "track_url": "assets/menu_theme.mp3"  # Points to your custom local file!
    }


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
        /* 🎬 CINEMATIC WIDESCREEN LIVE CANVAS COVER ART */
    .live-canvas-cover {
        width: 100% !important;
        max-height: 280px !important;
        object-fit: cover !important;
        border-radius: 18px !important;
        border: 1px solid rgba(124, 93, 250, 0.2);
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        margin-bottom: 20px !important;
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
        st.session_state.guest_tokens = 3  
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
            # Cleanly wipe the active visual background cover cache upon exiting the space
            if "world_cover_url" in st.session_state:
                st.session_state.world_cover_url = "https://picsum.photos"
            st.rerun()
            
        st.divider()

    
    # TOKEN COUNTER CHECKS
    if "user" in st.session_state:
        st.success(f"👑 PREMIUM PILOT: {st.session_state.user.email}")
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
    

    # SETTINGS SUB CONTAINER
    # 🎵 SYSTEM AUDIO MATRICES DECK
    with st.expander("🎵 AMBIENT AUDIOSCAPE", expanded=True):
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
                # Automatically loops through alternative high-quality background ambient sound nodes
                current_track = st.session_state.audio_state["track_url"]
                next_track = "https://google.com" if "ambient_hum" in current_track else "https://google.com"
                st.session_state.audio_state["track_url"] = next_track
                st.session_state.audio_state["playing"] = True
                st.rerun()
                
        # Hidden native HTML audio playback injector loop node
                        # 🎛️ NATIVE AUDIO INTERFACE CONTROL BOARD
        if st.session_state.audio_state["playing"]:
            # Streamlit's official built-in player that safely streams web tracks with zero errors
            st.audio(st.session_state.audio_state['track_url'], format="audio/mp3", loop=True)
            st.caption("🔊 Click play on the official media deck above to activate audio")
        else:
            st.markdown("<p style='font-size: 11px; text-align: center; color: #7f1d1d; margin: 10px 0 0 0; font-weight: bold;'>⚠️ System Audio Channel Disabled 🔴</p>", unsafe_allow_html=True)


    with st.expander("⚙️ SETTINGS CONTROL"):
            # 🎵 SYSTEM AUDIO MATRICES DECK
     with st.expander("🎵 AMBIENT AUDIOSCAPE", expanded=True):
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
                current_track = st.session_state.audio_state["track_url"]
                # Seamlessly swaps between your two custom local files
                next_track = "assets/adventure_loop.mp3" if "menu_theme" in current_track else "assets/menu_theme.mp3"
                st.session_state.audio_state["track_url"] = next_track
                st.session_state.audio_state["playing"] = True
                st.rerun()
                
        # Native Streamlit audio player optimized for local repository tracks
        if st.session_state.audio_state["playing"]:
            st.audio(st.session_state.audio_state['track_url'], format="audio/mp3", loop=True)
            st.caption("🔊 Press play above to authorize your custom stream")
        else:
            st.markdown("<p style='font-size: 11px; text-align: center; color: #7f1d1d; margin: 10px 0 0 0; font-weight: bold;'>⚠️ System Audio Channel Disabled 🔴</p>", unsafe_allow_html=True)

        st.caption("🔒 Sandbox Platform Environment Stable")
        st.markdown("<p style='font-size: 13px; color: #334155; font-style: italic;'>No legal frameworks or terms protocols mapped to this local sandbox node yet.</p>", unsafe_allow_html=True)
        
    st.divider()
    
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
                                    supabase_client.table("worlds").delete().eq("id", my_row["id"]).execute()
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
        st.markdown("### Universe Architect Form")
        w_name = st.text_input("Name your universe:", placeholder="e.g., Sector 7, Neo-Tokyo")
        w_genre = st.selectbox("Select thematic genre:", ["Sci-Fi", "Dark Fantasy", "Cyberpunk", "Horror", "Romance", "Other"])
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
        st.markdown("### Community Avatars Portal")
        st.caption("Click 'Inspect File' to view full resolution profiles and creator records.")
        
        cols_avatars = st.columns(3)
        with cols_avatars[0]:
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
        with cols_avatars[1]:
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
        with cols_avatars[2]:
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
                if st.button("🔓 Authenticate Profile", key="main_hub_auth_gateway_redirect", use_container_width=True):
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
    st.subheader("💳 Activate Subscription")
    st.info("Your free trial action points have been exhausted. Unlock the $10/week Pass to continue.")
    if st.button("👑 Get Unlimited Pass ($10/wk)", type="primary", use_container_width=True):
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Haymaker Unlimited Pass'},
                        'unit_amount': 1000, 'recurring': {'interval': 'week'}
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

# 8. INITIAL COSMOS ENTRY SCENE SPARK (WITH VALID DALL-E 3 GENERATION)
if not engine["story_log"]:
    if "world_cover_url" not in st.session_state:
        st.session_state.world_cover_url = "https://picsum.photos" # Default clean fallback state

    with st.spinner("⏳ Simulating initial cosmos entry scene & forging visual assets..."):
        try:
            image_prompt = f"Cinematic widescreen matte game concept background for an alternate reality adventure titled '{engine['world_name']}' in the genre of '{engine['world_genre']}'. Vivid colors, epic landscape, beautiful atmospheric light, zero text, zero labels, high resolution."
            img_response = openai_client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                n=1,
                size="1024x1024",
                quality="standard"
            )
            st.session_state.world_cover_url = img_response.data[0].url

        except Exception as img_err:
            st.warning(f"Visual Grid Warning: Defaulting to standard theme skin. ({img_err})")

        master_prompt = (
            f"You are the master narrator for a text adventure game called Haymaker.\n"
            f"World: '{engine['world_name']}' | Genre: '{engine['world_genre']}'.\n"
            f"Character: '{char['name']}' | Backstory: '{char['backstory']}'.\n"
            f"Inventory: {', '.join(char['inventory'])} | Health: {char['health']}/100.\n\n"
            f"⚠️ CRITICAL GAMEPLAY & FORMATTING RULES:\n"
            f"1. Be extremely concise. Deliver exactly ONE detailed short paragraph. Maximum 3 sentences.\n"
            f"2. Never play for the user or repeat their setup words. Establish the opening scene and stop instantly.\n"
            f"3. MULTI-CHARACTER FORMAT: If an NPC character speaks, format it on a new line exactly like this: CharacterName: **\"Dialogue text here\"** in standard bold."
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

# 9. INJECT DYNAMIC IMMERSIVE VISUAL BACKGROUND WINDOW WRAPPER
bg_url = st.session_state.world_cover_url
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

# Cleanly seal our custom HTML viewport scroller tags at script termination
st.markdown('</div></div>', unsafe_allow_html=True)
