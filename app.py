import streamlit as st
from logic_utils import create_game,get_attempt_limit,get_hint,get_range_for_difficulty,submit_guess
from ai_tutor import explain
st.set_page_config(page_title="Game Glitch Investigator AI",page_icon="🎮")
def reset():
    st.session_state.game=create_game(st.session_state.difficulty)
    st.session_state.guess_input=""
    st.session_state.error=None
def submit():
    st.session_state.game,st.session_state.error=submit_guess(st.session_state.game,st.session_state.guess_input)
st.title("🎮 Game Glitch Investigator AI")
st.caption("Play the fixed game, then learn how to debug its common bugs with a retrieval-grounded tutor.")
st.sidebar.selectbox("Difficulty",["Easy","Normal","Hard"],index=1,key="difficulty",on_change=reset)
if 'game' not in st.session_state: reset()
game=st.session_state.game
low,high=get_range_for_difficulty(st.session_state.difficulty)
st.info(f"Guess a whole number from {low} to {high}. Attempts left: {get_attempt_limit(game['difficulty'])-game['attempts']}")
with st.expander("Developer debug info (for testing)"):
    st.write(game)
finished=game['status']!='playing'
st.text_input("Enter your guess",key="guess_input",disabled=finished)
a,b=st.columns(2)
with a: st.button("Submit Guess",on_click=submit,disabled=finished)
with b: st.button("New Game",on_click=reset)
st.metric("Score",game['score'])
if st.session_state.error:st.error(st.session_state.error)
elif game['status']=='won':st.success(f"You won! Secret: {game['secret']}")
elif game['status']=='lost':st.error(f"Out of attempts. Secret: {game['secret']}")
elif game['last_outcome']:st.warning(get_hint(game['last_outcome']))
st.divider()
st.header("🧠 AI Debugging Tutor")
st.write("Describe a bug in the guessing game. The tutor retrieves a relevant reference and suggests a fix and test. It never runs your code.")
question=st.text_area("Bug description",placeholder="Easy mode accepts 99 and the secret is outside the range")
use_llm=st.checkbox("Use optional OpenAI-generated explanation (requires OPENAI_API_KEY)",value=False)
if st.button("Investigate bug"):
    result=explain(question,use_llm=use_llm)
    if result['status']=='ok':
        st.success("Reference matched")
        st.write(result['answer'])
        st.caption(f"Source: {result['source']} | Retrieval score (not probability): {result['confidence']} | Mode: {result['mode']} | Reference verified: {result['verified']}")
        st.info("Human review required: run the suggested test and inspect the code before accepting the fix.")
    else:st.warning(result['answer'])
