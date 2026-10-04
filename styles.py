GLOBAL_CSS = """
/* === 🌌 GLOBAL THEME DESIGN & GLASS CONFIGURATIONS === */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0c081c !important;
    background-image: radial-gradient(circle at 50% 0%, #1c133a 0%, #0c081c 70%) !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}

/* Force margins and layouts to utilize 100% of physical glass width on mobile grids */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* Make custom HTML horizontal block grids stack vertically on mobile browser screens */
@media (max-width: 768px) {
    .stHorizontalBlock { display: flex; flex-direction: column !important; }
    div[data-testid="column"] { width: 100% !important; margin-left: 0 !important; }
}

/* Custom dark-glass container borders */
.stExpander, div[data-testid="stForm"] {
    background: rgba(16, 12, 31, 0.4) !important;
    border-radius: 12px !important;
    border: 1px solid #2e234e !important;
    backdrop-filter: blur(10px) !important;
}
"""

CHAT_CSS = """
/* === ✍️ INTERACTIVE CHAT NARRATIVE BUBBLE INTERFACES === */
.chat-row-user {
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
    margin-bottom: 1rem;
    width: 100%;
}

.glass-bubble-user {
    background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%) !important;
    color: #ffffff !important;
    padding: 12px 16px !important;
    border-radius: 16px 16px 4px 16px !important;
    max-width: 75%;
    font-size: 14px !important;
    line-height: 1.5 !important;
    box-shadow: 0 4px 12px rgba(109, 40, 217, 0.2) !important;
    border: 1px solid #7c3aed !important;
}

.chat-row-ai {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    margin-bottom: 1rem;
    width: 100%;
}

.glass-bubble-ai {
    background: rgba(30, 27, 75, 0.4) !important;
    color: #e2e8f0 !important;
    padding: 12px 16px !important;
    border-radius: 16px 16px 16px 4px !important;
    max-width: 75%;
    font-size: 14px !important;
    line-height: 1.5 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    border: 1px solid #1e1b4b !important;
    backdrop-filter: blur(8px) !important;
}

.avatar-box {
    font-size: 20px !important;
    padding: 0 10px !important;
    display: flex;
    align-items: center;
    justify-content: center;
}
"""
