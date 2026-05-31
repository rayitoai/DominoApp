import streamlit as st

# Set page configuration to wide/responsive by default
st.set_page_config(page_title="Domino Scoreboard", layout="centered")

# 1. Initialize App State
if "teams" not in st.session_state:
  st.session_state.teams = [
  {"name": "Team Alpha", "score": 0},
  {"name": "Team Bravo", "score": 0},
  {"name": "Team Charlie", "score": 0},
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
st.toast("🚨 Nothing left to undo!")

def add_new_team():
save_to_history()
new_team_num = len(st.session_state.teams) + 1
st.session_state.teams.append({"name": f"Team {new_team_num}", "score": 0})

def reset_all():
st.session_state.teams = [
{"name": "Team Alpha", "score": 0},
{"name": "Team Bravo", "score": 0},
]
st.session_state.history = []

# 3. UI Layout
st.title("🎴 Domino Scoreboard")

# Global Controls - Stacked in 3 columns that adapt well to mobile
col_add, col_undo, col_reset = st.columns(3)
with col_add:
st.button("➕ Team", on_click=add_new_team, use_container_width=True)
with col_undo:
st.button("↩️ Undo", on_click=undo_last, use_container_width=True, type="primary")
with col_reset:
st.button("🔄 Reset", on_click=reset_all, use_container_width=True)

st.divider()

# 4. Live Winner Announcement (Moved to the top for immediate mobile visibility)
highest_score = max(team["score"] for team in st.session_state.teams)
winners = [team["name"] for team in st.session_state.teams if team["score"] == highest_score]

if len(winners) == 1:
st.success(f"👑 **Leader:** {winners[0]} ({highest_score} pts)")
else:
st.info(f"🤝 **Tie for 1st:** {', '.join(winners)} ({highest_score} pts)")

st.divider()

# 5. Dynamic Scoreboard Matrix (Mobile-Optimized Rows)
st.subheader("📋 Live Scores")

for idx, team in enumerate(st.session_state.teams):
# Using a 2-column card-like layout for each team
col_card_left, col_card_right = st.columns([5, 4])

with col_card_left:
# Large text input for the team name
new_name = st.text_input(
f"Team {idx+1} Name",
value=team["name"],
key=f"name_{idx}",
label_visibility="collapsed"
)
if new_name != team["name"]:
save_to_history()
st.session_state.teams[idx]["name"] = new_name
st.rarun()

with col_card_right:
# Native number input provides large, easy-to-tap minus/plus stepper buttons on mobile
new_score = st.number_input(
f"Score {idx}",
value=team["score"],
step=1,
key=f"score_in_{idx}",
label_visibility="collapsed"
)
if new_score != team["score"]:
save_to_history()
st.session_state.teams[idx]["score"] = new_score
st.rerun()

st.markdown("---") # Thin separator between teams for clarity on small screens
