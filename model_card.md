# Model Card and Responsible AI Reflection

## 1. Intended purpose and system boundary

**Game Glitch Investigator AI** is a learning-oriented debugging aid for five documented bug types in the CodePath Module 1 Python/Streamlit number-guessing game. It accepts a plain-language bug description, classifies the known issue, retrieves supporting snippets from a local ten-document curated corpus using category-filtered BM25, and proposes a diagnosis, fix, and test. It also offers a bounded, read-only workflow with an allowlisted game-invariant check.

**Default mode:** deterministic classification, BM25 document retrieval, and evidence-grounded templates. It is **not a generative language model**. **Optional model mode:** if the application owner privately configures `OPENAI_API_KEY`, the app can request an OpenAI explanation grounded in retrieved evidence; model availability, performance, and live-model accuracy have not been established by deterministic tests.

## 2. Data sources and provenance

The project includes `knowledge.py` (five manually documented issue categories) and `knowledge_docs.py` (ten short curated reference notes with relevant URLs to Python, Streamlit, and local project source documentation). These are **locally authored summaries and links**, not dynamically downloaded or verified full external webpages. Document ranking scores are BM25 relevance heuristics, not probabilities or evidence that a diagnosis is correct.

The displayed source IDs and links let a reviewer investigate a proposed cause. The classifier limits the retriever to the selected issue category, so an incorrect classification can cause apparently convincing but irrelevant evidence.

## 3. Limitations and biases

- Only five game-specific categories and a small English-language corpus are supported. General debugging requests may fail or be wrongly classified.
- Keyword-based issue classification can misinterpret paraphrases, mixed symptoms, and incomplete descriptions. The BM25 ranking is not a general semantic understanding system.
- The specialist six-field JSON report guarantees a **format contract**; high field coverage does not measure factual correctness.
- Tests of existing game invariants cannot prove an unimplemented fix will work.
- Prompt-injection filters are heuristic and not comprehensive.
- LLM-grounded outputs may hallucinate or misinterpret evidence. Generated explanations have not been independently scored.

## 4. Misuse and safety controls

The application rejects empty, oversized, and some malicious prompts; requests additional information for weak matches; avoids running any user-provided code; uses a fixed allowlist of safe invariant checks; never modifies a repository automatically; and requires human review. It uses environment variables for optional model credentials rather than placing keys in source code. Do not paste API keys, tokens, or private application code into the bug-description box. Optional LLM input is transmitted to the model provider when enabled.

These mitigations reduce—but do not eliminate—the possibility of inappropriate outputs or misuse.

## 5. Reliability testing: reproducible results and surprises

**Verified in GitHub Actions on November 5, 2026, at commit `efc6b65` (run [41945465729](https://github.com/harshapriyag123/game-glitch-investigator-ai/actions/runs/41945465729)):**
- `python -m pytest -q`: **30 tests passed**.
- `python evaluate.py`: **21/21 deterministic scenarios passed**.
- Retrieval evidence: **5/5 known issue examples gained supporting documents**.
- Structured specialization: **30/30 populated required field slots versus 0/30 in the free-form baseline**. **This measures output structure, not correctness.**

The workflow also generated valid JSON execution evidence as a downloadable `codepath-ai110-evidence` artifact. See the latest GitHub Actions run for the outcome after subsequent changes. A surprising boundary is that the system can safely decline unknown or suspicious input instead of inventing a diagnosis. Conversely, a clean structured response can still be wrong if the input is misclassified, and a passing invariant check does not validate a proposed patch.

These are predefined examples. There is no held-out human-annotated bug corpus, and no quantified generalization or live-LLM accuracy claim.

## 6. AI collaboration: student confirmation required

The following statements are **drafts grounded in the implementation and discussion, not independently verified first-person experience**. Review and edit them before submitting.

**How I collaborated with AI — draft:** I used AI assistance to refine the project's component design, reason about retrieval-based explanations, identify guardrails, design reproducible evaluations, and improve the Streamlit and GitHub documentation. I reviewed the proposed approach against CodePath's requirements and used the resulting code and tests to check that the features integrate into a working application.

**Suggestion accepted — draft:** Separate Streamlit presentation, issue knowledge, retrieval, evaluation, and game rules into independent modules. I accepted this modular architecture because it makes the end-to-end flow easier to inspect, test, and explain.

**Suggestion revised — draft:** Rather than implementing a coding agent that runs arbitrary submitted snippets or automatically patches files, I kept the debugging workflow read-only and restricted verification to predefined tests of existing game invariants. I changed this scope to avoid unintended code execution and inaccurate claims of auto-repair.

**What I learned — draft:** Trustworthy AI-assisted software requires a measurable baseline, traceable evidence, explicit handling of unknown inputs, transparency about model use, and human verification. High schema coverage is useful, but is not the same as factual accuracy.

**Before submission:** Confirm that the accepted/revised suggestions and your reasons accurately reflect what actually happened while building the project; edit any inaccurate first-person detail.

## 7. What the extra-credit comparisons demonstrate

| Capability | Baseline | Enhancement | What is actually measured |
|---|---|---|---|
| Retrieval | One matched issue with a template | Category-filtered BM25 returns cited curated documents | Retrieved source count and answer change, not an accuracy uplift |
| Agentic workflow | One-shot diagnosis | Six-step bounded planning, retrieved references, allowlisted test | Real tool-check status and auditable step summaries; not autonomous code fixing |
| Specialization | Free-form narrative | Schema-constrained six-field specialist report | Required machine-readable field coverage |
| Evaluation | Ad hoc outputs | Repeatable unit tests and 21-case deterministic harness | Pass/fail on fixed cases, not arbitrary unseen inputs |

## 8. Human oversight and future validation

A reviewer should independently read source documentation, run the suggested tests against their own change, and verify each fix. Future work should test held-out bug reports, perform human scoring for explanation correctness, measure false positives, verify links against the upstream documentation, and compare live-LLM outputs against deterministic results.
