# Model Card and Responsible AI Reflection

## Purpose and system boundary
Game Glitch Investigator AI helps learners recognize common bugs in a number-guessing game. It retrieves one of five curated references and can optionally ask an OpenAI model to explain the reference. Default operation is deterministic retrieval plus a template, **not** generative AI. The optional model is required to demonstrate actual LLM generation.

## Limitations and biases
The small English-language knowledge base covers five known issues, not arbitrary Python defects. Keyword retrieval can misclassify vague or multi-issue descriptions. The retrieval score is a heuristic, not calibrated confidence or proof that a proposed fix works. Optional LLM explanations can hallucinate despite grounded prompting.

## Misuse prevention
The app rejects empty/oversized descriptions and common prompt-injection phrases. It never executes user-submitted code or automatically modifies a repository. Secrets are not sent to the tutor. An API key must be configured in the environment, not committed. Human review and independent tests are required before applying suggestions. These controls reduce risk but are not comprehensive prompt-injection protection.

## Reliability testing and surprises
Verified local testing on November 4, 2026:
- `python -m pytest -q`: **11 passed**.
- `python evaluate.py`: **8/8 passed** (five known issue matches, three guardrail/rejection scenarios).
The interesting reliability boundary is that an unmatched bug produces a request for more context rather than an invented diagnosis. Retrieval can still produce false positives; these tests do not establish accuracy on arbitrary real-world bug reports.

## Collaboration with AI — personalize before submission
**Accepted suggestion (draft; confirm it reflects your actual work):** Separate bug knowledge and retrieval logic from the Streamlit interface so each can be tested independently.

**Revised or rejected suggestion (draft; confirm it reflects your actual work):** Instead of automatically executing AI-proposed code fixes, keep the tutor advisory-only with explicit human verification, reducing security and correctness risks.

**My own reflection (edit into your own voice):** I learned that a useful AI application needs measurable behavior, traceable sources, explicit failure handling, and clear human oversight, not just fluent explanations.

## Evaluation scope
The deterministic tests evaluate reference selection and guardrail behavior; they do not measure generative-model factual accuracy. If using the optional LLM, manually evaluate several real outputs and record pass/fail judgments here.
