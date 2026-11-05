# AI interaction and trace evidence

The system exposes source IDs, retrieval scores, and generation mode in its UI. These are auditable decision summaries, not hidden model chain-of-thought.

## Sample retrieval trace
```text
Input: The secret resets on every Streamlit rerun
Validation: accepted
Best match: secret_reset
Mode: retrieval-template
Human review: required before changing code
```

For extra-credit agentic traces, implement and record a real multi-step agent workflow first; the current system does not claim agentic behavior.

## Development collaboration
See `model_card.md` for draft accepted/revised suggestions; personalize them to match your actual AI-assisted development process before submission.
