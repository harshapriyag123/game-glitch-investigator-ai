from streamlit.testing.v1 import AppTest

def test_streamlit_starts_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY",raising=False)
    app=AppTest.from_file(str(__import__("pathlib").Path(__file__).resolve().parents[1]/"app.py"),default_timeout=30).run()
    assert not app.exception
    assert len(app.tabs)==5
