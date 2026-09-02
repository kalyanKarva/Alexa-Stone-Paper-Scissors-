"""
Stone Paper Scissors — Streamlit Web App
Run with:  streamlit run app.py

Required elements covered:
- Menu with Stone / Paper / Scissors          -> three buttons
- Accepts user's choice                        -> button click
- Random computer choice                       -> random.choice()
- Compares choices & decides winner            -> decide_winner()
- Displays both choices                        -> shown after each round
- Displays User wins / Computer wins / Draw    -> success/error/info box
- Multiple rounds                              -> session_state persists
- Live scoreboard for user & computer          -> st.metric
- Invalid choices prevented                    -> only buttons can be clicked,
                                                   so an invalid value can
                                                   never reach the game logic
- Option to exit                               -> "Exit Game" button + summary
"""

import random
import streamlit as st

CHOICES = ["Stone", "Paper", "Scissors"]
EMOJI = {"Stone": "🪨", "Paper": "📄", "Scissors": "✂️"}
BEATS = {"Stone": "Scissors", "Paper": "Stone", "Scissors": "Paper"}

st.set_page_config(page_title="Stone Paper Scissors", page_icon="✊")


def init_state():
    defaults = {
        "user_score": 0,
        "computer_score": 0,
        "rounds": 0,
        "game_over": False,
        "last_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def decide_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Draw"
    return "User" if BEATS[user_choice] == computer_choice else "Computer"


def play_round(user_choice):
    computer_choice = random.choice(CHOICES)
    winner = decide_winner(user_choice, computer_choice)

    st.session_state.rounds += 1
    if winner == "User":
        st.session_state.user_score += 1
    elif winner == "Computer":
        st.session_state.computer_score += 1

    st.session_state.last_result = {
        "user": user_choice,
        "computer": computer_choice,
        "winner": winner,
    }


def reset_game():
    for key in ("user_score", "computer_score", "rounds"):
        st.session_state[key] = 0
    st.session_state.game_over = False
    st.session_state.last_result = None


init_state()

st.title("✊ Stone Paper Scissors 📄✂️")
st.caption("Play against the computer — as many rounds as you like.")

if st.session_state.game_over:
    st.subheader("🏁 Game Over")
    st.write(
        f"**Final Score** — You: {st.session_state.user_score}  |  "
        f"Computer: {st.session_state.computer_score}  "
        f"(over {st.session_state.rounds} rounds)"
    )
    if st.session_state.user_score > st.session_state.computer_score:
        st.success("You won overall! 🎉")
    elif st.session_state.user_score < st.session_state.computer_score:
        st.error("Computer won overall! 🤖")
    else:
        st.info("It's an overall draw!")

    if st.button("🔄 Play Again", use_container_width=True):
        reset_game()
        st.rerun()

else:
    st.write("### Make your move")
    col1, col2, col3 = st.columns(3)
    if col1.button(f"{EMOJI['Stone']} Stone", use_container_width=True):
        play_round("Stone")
    if col2.button(f"{EMOJI['Paper']} Paper", use_container_width=True):
        play_round("Paper")
    if col3.button(f"{EMOJI['Scissors']} Scissors", use_container_width=True):
        play_round("Scissors")

    if st.session_state.last_result:
        r = st.session_state.last_result
        st.divider()
        st.write(
            f"**You:** {EMOJI[r['user']]} {r['user']}   vs   "
            f"**Computer:** {EMOJI[r['computer']]} {r['computer']}"
        )
        if r["winner"] == "Draw":
            st.info("🤝 It's a Draw!")
        elif r["winner"] == "User":
            st.success("🎉 You win this round!")
        else:
            st.error("🤖 Computer wins this round!")

    st.divider()
    s1, s2, s3 = st.columns(3)
    s1.metric("Your Score", st.session_state.user_score)
    s2.metric("Computer Score", st.session_state.computer_score)
    s3.metric("Rounds Played", st.session_state.rounds)

    st.divider()
    if st.button("🚪 Exit Game"):
        st.session_state.game_over = True
        st.rerun()
