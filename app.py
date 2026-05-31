import streamlit as st

st.set_page_config(page_title="Domino", layout="centered")

st.html("""
<style>
   [data-testid="stVerticalBlock"] {
       gap: 0.3rem !important;
   }
   .block-container {
       padding-top: 1.5rem !important;
       padding-bottom: 1rem !important;
   }
   header {
       visibility: hidden !important;
   }
   .safari-score {
       font-weight: 800 !important;
       color: #000000 !important;
       font-size: 1.4rem !important;
       display: block !important;
       text-align: center !important;
       line-height: 2.5rem !important;
       white-space: nowrap !important;
   }
   button[kind="secondary"], button[kind="primary"] {
       min-height: 3rem !important;
       font-size: 1.2rem !important;
   }
   button:active {
       transform: scale(0.95) !important;
       transition: transform 0.1s !important;
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
   st.session_state.history = []

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

def adjust_score(idx, amount):
   save_to_history()
   st.session_state.teams[idx]["score"] += amount

# 3. UI Layout
st.title("🁣🁤🁥🁦 Puntaje Dominó")

# Global Controls
col_add, col_undo, col_reset = st.columns(3)
with col_add:
   st.button("➕ Equipo", on_click=add_new_team, use_container_width=True)
with col_undo:
   st.button("↩️ Deshacer", on_click=undo_last, use_container_width=True, type="primary")
with col_reset:
   st.button("🔄 Reiniciar", on_click=reset_all, use_container_width=True)

st.divider()

# 4. Live Winner Announcement
highest_score = max(team["score"] for team in st.session_state.teams)
winners = [team["name"] for team in st.session_state.teams if team["score"] == highest_score]

if len(winners) == 1:
   st.success(f"👑 **Líder:** {winners[0]} ({highest_score} pts)")
else:
   st.info(f"🤝 **Empate en 1er lugar:** {', '.join(winners)} ({highest_score} pts)")

st.divider()

# 5. Scoreboard
st.subheader("📋 Puntuación Actual")

for idx, team in enumerate(st.session_state.teams):
   # Row 1: Name + Score
   col_name, col_score = st.columns([3, 1])
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
       st.html(f'<span class="safari-score">{team["score"]} pts</span>')

   # Row 2: Buttons
   col_minus, col_plus = st.columns(2)
   with col_minus:
       st.button("➖", key=f"minus_{idx}", on_click=adjust_score,
                 args=(idx, -1), use_container_width=True)
   with col_plus:
       st.button("➕", key=f"plus_{idx}", on_click=adjust_score,
                 args=(idx, 1), use_container_width=True)

   st.divider()
Dont do anyhting just hold this
