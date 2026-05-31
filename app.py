import streamlit as st

# Set page configuration to wide/responsive by default
st.set_page_config(page_title="Domino", layout="centered")

# Safe CSS to force single-line layout and remove vertical gaps on mobile
st.html("""
<style>
    /* Reduces vertical padding and margins to fit more teams on screen */
    [data-testid="stVerticalBlock"] {
        gap: 0.3rem !important;
    }
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 1rem !important;
    }
    header {
        visibility: hidden !important;
    }

    /* Target the text element to align nicely with the inputs */
    .score-text p {
        font-weight: 800 !important;
        color: #000000 !important;
        font-size: 1.1rem !important;
        line-height: 2.5rem !important;
        margin: 0 !important;
        white-space: nowrap !important;
    }

    /* CRITICAL MOBILE OVERRIDE: Forces rows to stay horizontal on mobile screens */
    @media (max-width: 640px) {
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            width: 100% !important;
            align-items: center !important;
            gap: 0.3rem !important;
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

# 5. Dynamic Scoreboard Matrix (Mobile-Optimized Rows)
st.subheader("📋 Puntuación Actual")

for idx, team in enumerate(st.session_state.teams):
    # Left-to-right exact proportional columns locked on one line by CSS
    # Name (40%), Score Badge (20%), Minus (20%), Plus (20%)
    col_name, col_score, col_minus, col_plus = st.columns([4, 2, 2, 2])

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
        # Wrapped in a container div to apply the clean bold black text alignment safely
        st.html(f'<div class="score-text"><p><b>{team["score"]} pts</b></p></div>')

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
