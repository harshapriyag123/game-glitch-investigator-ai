"""Bounded, auditable debugging workflow. No arbitrary code execution."""
from ai_tutor import explain
from knowledge import BUGS

REFERENCE_BY_ID={item["id"]:item for item in BUGS}

def investigate(query, use_llm=False):
    """Analyze -> retrieve -> plan -> propose -> verify reference -> report.

    Verification checks the *reference and proposed test's availability*,
    not whether a suggested code fix works. All actions are read-only.
    """
    trace=[]
    trace.append({"step":"analyze","status":"done","detail":"Input received for validation; no code execution."})
    result=explain(query,use_llm=use_llm)
    if result["status"]!="ok":
        trace.append({"step":"retrieve","status":result["status"],"detail":result["answer"]})
        return {"status":result["status"],"trace":trace,"result":result,
                "verification":"Not run: no accepted reference.","approval":"Human review required"}
    source=result["source"]
    trace.append({"step":"retrieve","status":"done","detail":f"Matched curated reference {source}."})
    reference=REFERENCE_BY_ID.get(source)
    if reference is None:
        trace.append({"step":"verify","status":"failed","detail":"Source missing from allowlisted knowledge."})
        return {"status":"failed","trace":trace,"result":result,
                "verification":"Failed: unknown source.","approval":"Human review required"}
    trace.append({"step":"plan","status":"done","detail":"Use the curated root cause and proposed fix."})
    trace.append({"step":"propose","status":"done","detail":reference["fix"]})
    valid_test=bool(reference.get("test","").strip())
    trace.append({"step":"verify","status":"done" if valid_test else "failed",
                  "detail":"Reference and test instructions are present; fix has NOT been executed."
                  if valid_test else "No verification test documented."})
    trace.append({"step":"report","status":"done","detail":"Advisory report prepared for human review."})
    return {"status":"ready_for_review" if valid_test else "failed",
            "trace":trace,"result":result,"verification":reference.get("test",""),
            "approval":"Human review required; no patch applied"}
