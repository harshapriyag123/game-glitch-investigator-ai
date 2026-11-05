"""Streamlit UI for a playable game and auditable AI-assisted debugging."""
import streamlit as st
from logic_utils import create_game, get_attempt_limit, get_hint, get_range_for_difficulty, submit_guess
from debug_engine import explain_enhanced
from agent_workflow import investigate
from evaluate import evaluate_cases,extended_cases,retrieval_comparison
from specialization import schema_comparison,specialized_report

st.set_page_config(page_title="Game Glitch Investigator AI",page_icon="🎮",layout="wide",initial_sidebar_state="expanded")
st.markdown("""
<style>
.block-container {max-width:1200px;padding-top:1.6rem}
.hero {padding:1.4rem 1.7rem;background:linear-gradient(120deg,#14243c,#243c69);border-radius:18px;color:white;margin-bottom:1.5rem}
.hero h1 {margin:0;color:white;font-size:2.1rem}
.hero p {margin:.5rem 0 0;color:#d8e5ff}
[data-testid="stMetric"] {border:1px solid rgba(115,137,166,.28);border-radius:12px;padding:.65rem}
</style>
""",unsafe_allow_html=True)
def reset():
    st.session_state.game=create_game(st.session_state.difficulty)
    st.session_state.guess_input=""
    st.session_state.error=None
def submit():
    st.session_state.game,st.session_state.error=submit_guess(st.session_state.game,st.session_state.guess_input)
st.markdown('<div class="hero"><h1>🎮 Game Glitch Investigator AI</h1><p>Play the game · Find the evidence · Verify the fix · Learn safely</p></div>',unsafe_allow_html=True)
with st.sidebar:
    st.subheader("Project navigation")
    st.selectbox("Difficulty",["Easy","Normal","Hard"],index=1,key="difficulty",on_change=reset)
    st.caption("CodePath AI110 · Applied AI System")
    st.link_button("Source on GitHub","https://github.com/harshapriyag123/game-glitch-investigator-ai")
    st.info("Works offline with retrieved documents. Optional OpenAI explanations require an API key.")
if "game" not in st.session_state:reset()
game=st.session_state.game
tabs=st.tabs(["🎯 Game Arena","🧠 AI Debugging Lab","🔍 Agent Workflow","📊 Evaluation","ℹ️ About"])
with tabs[0]:
    st.subheader("Guess the secret number")
    low,high=get_range_for_difficulty(game["difficulty"])
    available=get_attempt_limit(game["difficulty"])-game["attempts"]
    m1,m2,m3,m4=st.columns(4)
    m1.metric("Mode",game["difficulty"])
    m2.metric("Range",f"{low}–{high}")
    m3.metric("Attempts left",available)
    m4.metric("Score",game["score"])
    st.text_input("Enter an integer guess",key="guess_input",disabled=game["status"]!="playing")
    c1,c2=st.columns(2)
    c1.button("Submit guess",key="guess_submit",on_click=submit,disabled=game["status"]!="playing",use_container_width=True)
    c2.button("New game",key="new_game",on_click=reset,use_container_width=True)
    current=st.session_state.game
    if st.session_state.error:st.error(st.session_state.error)
    elif current["status"]=="won":st.success(f"Correct! The secret was {current['secret']}.")
    elif current["status"]=="lost":st.warning(f"Round finished. The secret was {current['secret']}.")
    elif current["last_outcome"]:st.info(get_hint(current["last_outcome"]))
    if current["history"]:
        st.caption("Previous valid guesses: "+", ".join(map(str,current["history"])))
with tabs[1]:
    st.subheader("Retrieval-grounded debugging tutor")
    st.write("Investigate a known game bug with source-backed evidence. The tutor proposes fixes but never applies them.")
    example=st.selectbox("Example reports",["Custom report","The secret resets on every Streamlit rerun","Easy mode accepts 99 and uses the wrong range","Blank or abc input consumes an attempt","New Game does not clear my score"])
    prompt=st.text_area("Describe the symptom",value="" if example=="Custom report" else example,key="bug_report",height=110)
    use_llm=st.checkbox("Use optional OpenAI explanation (requires server API key)",key="bug_llm")
    if st.button("Investigate bug",type="primary",key="investigate_bug"):
        st.session_state["tutor_report"]=explain_enhanced(prompt,use_llm=use_llm)
        st.session_state["specialist_report"]=specialized_report(prompt)
    if "tutor_report" in st.session_state:
        output=st.session_state["tutor_report"]
        if output["status"]=="ok":
            st.success("Matched curated game issue")
            st.code(output["answer"],language="text")
            st.caption(f"Source issue: {output['source']} · Mode: {output['mode']} · Matching heuristic: {output['confidence']} (not calibrated probability)")
            with st.expander("Source documents and retrieval scores",expanded=True):
                for doc in output.get("documents",[]):
                    st.markdown(f"**{doc['title']}** · [Reference]({doc['url']}) · BM25 score: {doc['score']}")
                    st.write(doc["text"])
            with st.expander("Machine-readable specialist report"):
                fields=st.session_state.get("specialist_report",{}).get("fields")
                if fields:st.json(fields)
            st.warning("Human review required: the explanation is advisory, not a verified patch.")
        else:st.warning(output["answer"])
with tabs[2]:
    st.subheader("Safe, bounded debugging workflow")
    st.caption("Analyze → Retrieve → Plan → Propose → Run allowlisted check → Report. Tests validate existing game invariants, not the suggested patch.")
    agent_query=st.text_area("Bug report",placeholder="The secret changes with every guess",key="agent_input")
    if st.button("Run debugging workflow",key="agent_run"):
        st.session_state["agent_result"]=investigate(agent_query)
    if "agent_result" in st.session_state:
        run=st.session_state["agent_result"]
        st.write(f"**Workflow status:** {run['status']}")
        st.dataframe([{"Stage":item["step"],"Status":item["status"],"What happened":item["detail"]} for item in run["trace"]],hide_index=True,use_container_width=True)
        if run.get("verification_run"):
            st.write("**Allowlisted verification result**")
            st.json(run["verification_run"])
        st.info("Suggested independent check: "+run["verification"])
        st.warning(run["approval"])
with tabs[3]:
    st.subheader("Deterministic reliability dashboard")
    st.caption("Results are computed on demand from predefined tests. They do not measure live LLM quality.")
    if st.button("Run evaluation suite",key="eval_run",type="primary"):
        st.session_state["evaluation_results"]=evaluate_cases()+extended_cases()
        st.session_state["retrieval_comparison"]=retrieval_comparison()
        st.session_state["schema_comparison"]=schema_comparison([
            "The secret resets on every Streamlit rerun",
            "Why does Easy mode accept 99 and have the wrong range?",
            "Blank and abc invalid input uses an attempt",
            "New game keeps score and history after restart",
            "Comparing string numbers gives wrong higher lower hint"])
    if "evaluation_results" in st.session_state:
        rows=st.session_state["evaluation_results"]
        good=sum(bool(r["pass"]) for r in rows)
        a,b,c=st.columns(3)
        a.metric("Scenarios",len(rows))
        b.metric("Passing",good)
        c.metric("Failing",len(rows)-good)
        st.dataframe([{"Scenario":r["case"],"Result":"PASS" if r["pass"] else "FAIL",
                       "Details":r.get("detail",r.get("actual_status",""))} for r in rows],hide_index=True,use_container_width=True)
        st.markdown("#### Baseline versus document-backed retrieval")
        st.dataframe(st.session_state["retrieval_comparison"],hide_index=True,use_container_width=True)
        st.markdown("#### Baseline versus specialist schema coverage")
        st.dataframe(st.session_state["schema_comparison"],hide_index=True,use_container_width=True)
        st.caption("Comparison measures source coverage and machine-readable format, not factual accuracy or generalization.")
with tabs[4]:
    st.subheader("How the system works")
    st.markdown("""
**Goal.** Extend the original CodePath Module 1 guessing game with evidence-based debugging guidance.

**Pipeline.** Validate → match known issue → BM25 retrieve supporting local documents → explain and cite → select a predefined game invariant check → return a human-reviewed report.

**Architecture.** The editable source diagram is at [diagrams/architecture.mmd](https://github.com/harshapriyag123/game-glitch-investigator-ai/blob/main/diagrams/architecture.mmd).

**Boundaries.** This prototype handles five documented bug categories. It is not a general coding assistant. Source scores are relevance heuristics, not calibrated confidence. Tests check existing code only. Optional LLM explanations require independent evaluation.

**Portfolio:** [README](https://github.com/harshapriyag123/game-glitch-investigator-ai#readme) · [Model card](https://github.com/harshapriyag123/game-glitch-investigator-ai/blob/main/model_card.md) · [Presentation](https://github.com/harshapriyag123/game-glitch-investigator-ai/blob/main/PRESENTATION.md).
""")
