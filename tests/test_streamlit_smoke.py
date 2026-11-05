from streamlit.testing.v1 import AppTest
from pathlib import Path

def test_streamlit_starts_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY",raising=False)
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/"app.py"),default_timeout=30).run()
    assert not app.exception
    assert len(app.tabs)==5

def test_streamlit_evaluation_button(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY",raising=False)
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/"app.py"),default_timeout=30).run()
    app.button(key="eval_run").click().run()
    assert not app.exception
    assert len(app.session_state["evaluation_results"])==21

def test_streamlit_agent_button(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY",raising=False)
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/"app.py"),default_timeout=30).run()
    app.text_area(key="agent_input").set_value("The secret resets on every Streamlit rerun").run()
    app.button(key="agent_run").click().run()
    assert not app.exception
    assert app.session_state["agent_result"]["status"]=="ready_for_review"
