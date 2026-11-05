# CodePath AI110 Module 5 Project 4 — Grading Readiness Report

**Prepared:** November 5, 2026. **Deadline:** November 16, 2026 at 1:59 AM CST.

**Original Module 1 project:** https://github.com/harshapriyag123/ai110-module1show-gameglitchinvestigator-starter

**Submission repo:** https://github.com/harshapriyag123/game-glitch-investigator-ai

**User-supplied hosted Streamlit app:** https://game-glitch-investigator-ai-5e7ftpz7mef2e9trsrwmta.streamlit.app/

This report is an audit of the *uploaded Week 9 assignment instructions* and actual project code, **not** an official CodePath grade. The detailed grading-page point allocation was not attached, so only the published **21 core-point total** and **four optional +2 items** are used. No score is guaranteed.

## Required project features (21-point core rubric)

| Requirement | Evidence | Status | Reviewer follow-up |
|---|---|---|---|
| Extend earlier Module 1–3 project | Module 1 link; playable game in `logic_utils.py` and `app.py` | Implemented | New repo is a separately built extension; original historical commits were not imported as the same Git ancestry |
| Public repository and meaningful commits | GitHub repository and commit history | Verified | None |
| End-to-end AI-integrated task | `debug_engine.py`, `app.py`, `agent_workflow.py` | Verified via CI and Streamlit AppTest | Optional live-LLM path unverified |
| Python modules and safety | `knowledge.py`, `knowledge_docs.py`, `retrieval_enhanced.py`, `verification_tools.py`, input validation | Verified for predefined tests | Human review for real-world usage |
| Mermaid source diagram | `diagrams/architecture.mmd` | Verified in repo | None |
| README structure and setup | `README.md` | Present | Verify instructions on your own machine if desired |
| 2–3 real input/output cases | `reproduce_evidence.py`, README text extracts, CI job logs | Verified in GitHub Actions | None |
| Reliability and guardrails | `tests/`, `evaluate.py`, simulated API failure and injection checks | Verified for deterministic suite | No claim about unknown-input generalization |
| Responsible AI and collaboration reflection | `model_card.md` | Draft available | **Student must personally confirm/rewrite first-person parts** |
| 5–7 minute presentation and portfolio paragraph | `PRESENTATION.md`, README portfolio statement | Outline ready | Student must actually present/record if requested |
| Submit before deadline | GitHub and hosted app links | Not submitted by assistant | Student must complete CodePath submission |

## Optional stretch features — up to +8

| Stretch | Maximum | Evidence | Verified behavior | Grader limitation |
|---|---:|---|---|---|
| Enhanced RAG | +2 | `knowledge_docs.py` + `retrieval_enhanced.py` + `debug_engine.py` | 5/5 known samples gain source notes; selected evidence changes the answer | No evidence of improved general classification accuracy; deterministic mode is not LLM generation |
| Multi-step agentic workflow | +2 | `agent_workflow.py` + `verification_tools.py` + `ai_interactions.md` | Six steps and actual safe allowlisted current-game checks | Does not generate/apply/test an arbitrary code patch |
| Fine-tuning or specialization | +2 | `specialization.py` + `evaluate.py` | 30/30 structured slots vs 0/30 baseline schema slots | Schema compliance, **not** factual-answer accuracy; no model fine-tuning |
| Evaluation harness | +2 | `evaluate.py` + `tests/` | 21/21 deterministic cases passed | Not a held-out benchmark or live LLM evaluation |

## Verified technical evidence

From [successful GitHub Actions run 41945106493](https://github.com/harshapriyag123/game-glitch-investigator-ai/actions/runs/41945106493):

```text
28 passed in 1.02s
RESULT: 21/21 passed (deterministic; no live model evaluated)
RETRIEVAL: 5/5 known inputs gained supporting documents
SPECIALIZATION: 30/30 structured field slots vs 0/30 baseline schema slots; measures format only
Streamlit AppTest: startup passed
```

The tests exercise known issue retrieval, empty/unknown/injection inputs, missing API key, mocked API outage, difficulty boundaries, safe allowlisted verification and Streamlit UI interactions. The numbers above are tied to that exact CI run; for subsequent commits, check [Actions](https://github.com/harshapriyag123/game-glitch-investigator-ai/actions).

To reproduce:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python evaluate.py
python reproduce_evidence.py
python -m streamlit run app.py
```

## Main development milestones

- `bc32d74` — curated multi-source BM25 retrieval, specialist output, safe verification.
- `95f583f` — five-tab Streamlit app, integrated evaluation, architecture and CI.
- `85597c7` — UI interaction tests.
- `81ded65` — evidence-based README, model card, workflow traces and presentation.
- `43ef449` — refreshed published test evidence.

## Verification boundaries and remaining actions

1. **Hosted Streamlit URL:** Provided by the student, but could not be independently loaded with the available browser tools. Confirm it reflects the latest `main` branch and that tabs/buttons work.
2. **Optional model:** No live `OPENAI_API_KEY` was used. Generated OpenAI output and its accuracy are unverified. Offline document-grounded mode works.
3. **Personal reflection:** `model_card.md` includes clearly marked suggested first-person drafts; students must confirm what actually happened and explain their own accepted/revised AI suggestion.
4. **Presentation:** Script prepared, but delivery/recording and CodePath submission require the student's own action.
5. **Claims:** Source coverage and specialist schema completeness do not establish increased factual correctness. Passing allowlisted checks of existing code do not prove an AI-suggested patch works.

## Submission recommendation

Submit the **public GitHub repository** and the **hosted Streamlit URL** before November 16, 2026 at 1:59 AM CST. Cite the README's three logged interactions and evaluation results. Edit the model card reflection personally and show the limitations rather than overclaiming extra-credit performance.
