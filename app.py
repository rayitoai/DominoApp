import streamlit as st

# Set page configuration to wide/responsive by default
st.set_page_config(page_title="Domino", layout="centered")

# Custom CSS using native st.html to perfectly position and hide elements
st.html("""
<style>
    /* Reduces space between rows and columns */
    [data-testid="stVerticalBlock"] {
        gap: 0.4rem !important;
    }
    [data-testid="stHorizontalBlock"] {
        gap: 0.4rem !important;
    }
    
    /* Safely pushes layout below the floating Streamlit deployment banner */
    .block-container {
        padding-top: 5rem !important;
        padding-bottom: 1.5rem !important;
    }
    
    /* Hides extraneous floating decoration lines at the absolute top of the page */
    header {
        visibility: hidden !important;
    }
    
    /* Custom styling for the bold black score badge - now aligns left close to name */
    .score-badge {
        font-weight: 800 !important;
        color: #000000 !important;
        font-size: 1.15rem;
        text-align: left !important;
        line-height: 2.5rem; /* Aligns vertically with the input box height */
        display: block;
        padding-left: 0.2rem;
    }

    /* Centers the custom button row and makes it half size */
    .custom-btn-row {
        display: flex !important;
        justify-content: center !important;
        gap: 1rem !important;
        width: 100% !important;
        margin: 0.2rem 0 !important;
    }

    /* Sets an exact smaller physical size for the buttons on mobile */
    .custom-mobile-btn {
        width: 70px !important;
        height: 42px !important;
        font-size: 1.2rem !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #b9bcc4 !important;
        border-radius: 8px !important;
        color: #31333F !important;
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    .custom-mobile-btn:active {
        background-color: #e0e2e6 !important;
    }
    
    /* HARD LOCK: Completely hides the fallback macro-buttons from Streamlit framework */
    div[data-testid="element-container"] button[id^="hidden-minus"],
    div[data-testid="element-container"] button[id^="hidden-plus"],
    .hidden-trigger-zone {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }
    
    /* GLOBAL MOBILE OVERRIDE: Forces top Name/Score row to stay horizontal */
    @media (max-width: 640px) {
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            width: 100% !important;
        }
        div[data-testid="column"] {
            flex: 1 1 auto !important;
            width: auto !important;
        }
    }
</style>
""")

# 1. Initialize App State
if "teams" not in st.session_state:
    st.session_state.teams = [
        {"name": "Equipo 1", "score": 0},
        {"name": "Equipo 2", "score": 0},
        {"name": "Equipo 3", "score": 0},
    ]
if "history" not in st.session_state:
    st.session_state.history = [] # Stores deep copies for Undo

# 2. Helper Functions
def save_to_history():
    snapshot = [team.copy() for team in st.session_state.teams]
    st.session_state.history.append(snapshot)

def undo_last():
    if st.session_state.history:
        st.session_state.teams = st.session_state.history.pop()
    else:
        st.toast("🚨 ¡No hay nada más que deshacer!")

def add_new_team():
    save_to_history()
    new_team_num = len(st.session_state.teams) + 1
    st.session_state.teams.append({"name": f"Equipo {new_team_num}", "score": 0})

def reset_all():
    st.session_state.teams = [
        {"name": "Equipo 1", "score": 0},
        {"name": "Equipo 2", "score": 0},
        {"name": "Equipo 3", "score": 0},
    ]
    st.session_state.history = []

# Inline score modification helpers
def adjust_score(idx, amount):
    save_to_history()
    st.session_state.teams[idx]["score"] += amount

# 3. UI Layout
st.title("🁣🁤🁥🁦 Puntaje Dominó")

# Global Controls - Stacked in 3 columns that adapt well to mobile
col_add, col_undo, col_reset = st.columns(3)
with col_add:
    st.button("➕ Equipo", on_click=add_new_team, use_container_width=True)
with col_undo:
    st.button("↩️ Deshacer", on_click=undo_last, use_container_width=True, type="primary")
with col_reset:
    st.button("🔄 Reiniciar", on_click=reset_all, use_container_width=True)

st.divider()

# 4. Live Winner Announcement (Moved to the top for immediate mobile visibility)
highest_score = max(team["score"] for team in st.session_state.teams)
winners = [team["name"] for team in st.session_state.teams if team["score"] == highest_score]

if len(winners) == 1:
    st.success(f"👑 **Líder:** {winners[0]} ({highest_score} pts)")
else:
    st.info(f"🤝 **Empate en 1er lugar:** {', '.join(winners)} ({highest_score} pts)")

st.divider()

# 5. Dynamic Scoreboard Matrix (Mobile-Optimized Vertical Stack)
st.subheader("📋 Puntuación Actual")

for idx, team in enumerate(st.session_state.teams):
    # --- ROW TOP LINE: Ratio shifted to [4, 1] to pull score closer to name ---
    col_name, col_score = st.columns([4, 1])
    
    with col_name:
        new_name = st.text_input(
            f"Nombre del Equipo {idx+1}",
            value=team["name"],
            key=f"name_{idx}",
            label_visibility="collapsed"
        )
        if new_name != team["name"]:
            save_to_history()
            st.session_state.teams[idx]["name"] = new_name
            st.rerun()

    with col_score:
        st.html(f'<span class="score-badge">{team["score"]} pts</span>')

    # --- ROW BOTTOM LINE: Custom HTML Buttons ---
    st.html(f"""
    <div class="custom-btn-row">
        <button class="custom-mobile-btn" onclick="document.getElementById('hidden_minus_{idx}').click()">➖</button>
        <button class="custom-mobile-btn" onclick="document.getElementById('hidden_plus_{idx}').click()">➕</button>
    </div>
    """)

    # Hidden macro elements isolated inside a class targeted directly by CSS display: none
    with st.container():
        st.html('<div class="hidden-trigger-zone">')
        st.button("hidden_minus", key=f"hidden_minus_{idx}", on_click=adjust_score, args=(idx, -1))
        st.button("hidden_plus", key=f"hidden_plus_{idx}", on_click=adjust_score, args=(idx, 1))
        st.html('</div>')
    
    # Tiny spacer element between card blocks
    st.write("")
