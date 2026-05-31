import streamlit as st

# Set page configuration to wide/responsive by default
st.set_page_config(page_title="Domino", layout="centered")

# Safe CSS to handle vertical spacing and text styling cleanly across all browsers
st.html("""
<style>
    /* Safely tighter layout gaps to fit more teams on a mobile screen */
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

    /* Cross-browser styling for the bold black points badge */
    .safari-score {
        font-weight: 800 !important;
        color: #000000 !important;
        font-size: 1.1rem !important;
        line-height: 2.5rem; /* Matches default text input height */
        white-space: nowrap !important;
        display: inline-block;
        margin: 0 !important;
        padding-left: 0.2rem;
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

# 5. Dynamic Scoreboard Matrix (Safari & Chrome Mobile Stable)
st.subheader("📋 Puntuación Actual")

for idx, team in enumerate(st.session_state.teams):
    # Splits row into 2 concrete blocks so Safari preserves the line flow perfectly
    col_identity, col_actions = st.columns([6, 4])

    # Left Block (60%): Holds Name input and your Bold Black Points badge inline
    with col_identity:
        sub_name, sub_score = st.columns([3.5, 2.5])
        with sub_name:
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
        with sub_score:
            st.html(f'<span class="safari-score">{team["score"]} pts</span>')

    # Right Block (40%): Holds the adjustment buttons strictly side-by-side
    with col_actions:
        sub_minus, sub_plus = st.columns(2)
        with sub_minus:
            st.button(
                "➖", 
                key=f"minus_{idx}", 
                on_click=adjust_score, 
                args=(idx, -1), 
                use_container_width=True
            )
        with sub_plus:
            st.button(
                "➕", 
                key=f"plus_{idx}", 
                on_click=adjust_score, 
                args=(idx, 1), 
                use_container_width=True
            )
