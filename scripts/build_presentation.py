"""Build the editable CodePath student presentation; run: pip install python-pptx && python scripts/build_presentation.py"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "deliverables" / "Game_Glitch_Investigator_AI_CodePath_Final_Presentation.pptx"
NAVY = RGBColor(17, 31, 55)
GOLD = RGBColor(244, 188, 85)
WHITE = RGBColor(246, 249, 255)
MUTED = RGBColor(191, 206, 227)

def write(slide, x, y, w, h, content, size=23, color=WHITE, bold=False):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.word_wrap = True
    for index, line in enumerate(content.split("\n")):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.font.size = Pt(size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = color
        paragraph.space_after = Pt(12)

def make_slide(pres, heading, points, footer="", size=22):
    slide = pres.slides.add_slide(pres.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = NAVY
    write(slide, .7, .45, 12, .8, heading, 34, GOLD, True)
    y = 1.4
    for point in points:
        write(slide, .9, y, 11.7, 1.15, "•  " + point, size)
        y += 1.1
    if footer:
        write(slide, .8, 6.85, 11.9, .4, footer, 12, MUTED)
    return slide

pres = Presentation()
pres.slide_width = Inches(13.333)
pres.slide_height = Inches(7.5)
slide = pres.slides.add_slide(pres.slide_layouts[6])
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = NAVY
write(slide, .85, 1.4, 11.6, 1.6, "GAME GLITCH\nINVESTIGATOR AI", 46, GOLD, True)
write(slide, .9, 4.15, 11.3, 1.1, "CodePath AI110 · Final Project 4\nFrom a number-guessing game to evidence-grounded debugging", 24)
write(slide, .9, 6.65, 11, .4, "Student presentation · Approximately 6 minutes", 15, MUTED)

make_slide(pres, "01  Problem & original project", [
    "Module 1: playable number-guessing game with Easy, Normal and Hard modes.",
    "Handled guesses, hints, score, attempt limits, input validation and resets.",
    "Final project goal: explain recurring bugs and show how to verify fixes."
], "DEMO: Game Arena — valid guess, invalid input, reset")
make_slide(pres, "02  Five integrated application areas", [
    "Game Arena — play and inspect current game state.",
    "AI Debugging Lab — report a symptom and inspect cited evidence.",
    "Agent Workflow — bounded steps, tool results and human review.",
    "Evaluation — real test results and baseline comparisons.",
    "About — architecture, scope, limitations and source repository."
], "DEMO: Navigate the five tabs")
make_slide(pres, "03  Architecture & responsible retrieval", [
    "Validate bug description → classify one of five known issue types.",
    "BM25 ranks ten locally curated debugging notes with source IDs and links.",
    "Return root cause, proposed fix, evidence and a verification suggestion.",
    "Optional OpenAI explanation; deterministic fallback works without a key."
], "SOURCE: diagrams/architecture.mmd", 21)
make_slide(pres, "04  End-to-end example: secret reset", [
    "Input: The secret resets on every Streamlit rerun.",
    "Retrieved evidence: st-rerun and st-session.",
    "Diagnosis: the random secret is regenerated on each rerun.",
    "Proposed fix: initialize once per round and preserve session state.",
    "Allowlisted current-game check passed; human review still required."
], "DEMO: AI Debugging Lab → Agent Workflow", 21)
make_slide(pres, "05  End-to-end example: difficulty limits", [
    "Input: Why does Easy mode accept 99 and have the wrong range?",
    "Retrieved evidence: range-limits and random-randint.",
    "Proposed fix: use inclusive mode-specific limits and reset on mode change.",
    "Verification: accept Easy 1 and 20; reject 0 and 21.",
    "Passing current-code checks do not prove a proposed patch was applied."
], "DEMO: Show retrieved sources and workflow trace", 21)
make_slide(pres, "06  Reliability & reproducible evidence", [
    "30 unit/UI tests passed in a verified GitHub Actions run.",
    "21/21 deterministic evaluation checks passed.",
    "5/5 known inputs gained supporting retrieved documents.",
    "Specialist format: 30/30 fields versus 0/30 baseline schema slots.",
    "These measure fixed cases, evidence coverage and format — not unseen-bug accuracy."
], "EVIDENCE: GitHub Actions run 41945465729", 20)
make_slide(pres, "07  Four optional enhancements", [
    "Enhanced RAG: curated multi-source notes, BM25 ranking and citations.",
    "Agentic workflow: analyze → retrieve → plan → propose → verify → report.",
    "Specialization: six-field debugging report with measurable schema coverage.",
    "Evaluation harness: security, fallback, workflow and retrieval test cases."
], "Extra-credit eligibility is determined by CodePath.", 21)
make_slide(pres, "08  Safety, limitations & next steps", [
    "Rejects suspicious instructions; does not execute arbitrary submitted code.",
    "Tests current game invariants, not hypothetical AI-generated patches.",
    "Five known categories, small English corpus and heuristic retrieval.",
    "Optional LLM path has not been independently evaluated live.",
    "Future work: held-out labeled reports, source checks and LLM benchmarking."
], "PERSONAL REFLECTION: Review model_card.md for your own collaboration details.", 20)
make_slide(pres, "09  Submission & closing", [
    "GitHub: github.com/harshapriyag123/game-glitch-investigator-ai",
    "Streamlit: game-glitch-investigator-ai-5e7ftpz7mef2e9trsrwmta.streamlit.app",
    "Reproduce: python -m pytest -q · python evaluate.py · python reproduce_evidence.py",
    "Documentation: README.md, model_card.md, ai_interactions.md, architecture.mmd.",
    "Deadline: November 16, 2026, 1:59 AM CST."
], "Thank you!", 19)
DEST.parent.mkdir(parents=True, exist_ok=True)
pres.save(DEST)
print(f"Generated {DEST}")
