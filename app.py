import streamlit as st

# Set page configuration to wide/responsive by default
st.set_page_config(page_title="Domino", layout="centered")

# Custom CSS using native st.html to prevent Python 3.14 parsing bugs
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
    
    /* Custom styling for the bold black score badge */
    .score-badge {
        font-weight: 800 !important;
        color: #000000 !important;
        font-size: 1.25rem;
        text-align: right;
        line-height: 2.5rem; /* Aligns vertically with the input box height */
        display: block;
        padding-right: 0.5rem;
    }
    
    /* Extra margin tightening for mobile card structures */
    div[data-testid="stBlock"] {
        margin-bottom: 0.2rem !important;
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

# Inline score modification helpers to keep code clean
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
    # --- ROW TOP LINE: Name input left (80%), Score badge right (20%) ---
    col_name, col_score = st.columns([8, 2])
    
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

    # --- ROW BOTTOM LINE: Big side-by-side action buttons directly underneath ---
    col_minus, col_plus = st.columns(2)
    
    with col_minus:
        st.button(
            "➖", 
            key=f"minus_{idx}", 
            on_click=adjust_score, 
            args=(idx, -1), 
            use_container_width=True
        )
        
    with col_plus:
        st.button(
            "➕", 
            key=f"plus_{idx}", 
            on_click=adjust_score, 
            args=(idx, 1), 
            use_container_width=True
        )
    
    # A light spacer between the team block clusters to keep it organized
    st.write("")
