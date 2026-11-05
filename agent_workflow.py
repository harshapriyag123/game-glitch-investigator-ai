"""Bounded debugging orchestrator: real retrieval and allowlisted verification."""
from debug_engine import explain_enhanced
from knowledge import BUGS
from verification_tools import verify_existing_game
REFERENCE_BY_ID={b["id"]:b for b in BUGS}
MAX_STEPS=6
def investigate(query,use_llm=False):
    """Never executes arbitrary user code, patches files, or exposes hidden model reasoning."""
    trace=[{"step":"analyze","status":"done","detail":"Input sent to length and instruction validation."}]
    result=explain_enhanced(query,use_llm=use_llm)
    if result["status"]!="ok":
        trace.append({"step":"retrieve","status":result["status"],"detail":result["answer"]})
        return {"status":result["status"],"trace":trace,"result":result,
                "verification":"Not run: no accepted reference.","verification_run":None,
                "approval":"Human review required"}
    bug=REFERENCE_BY_ID.get(result["source"])
    trace.append({"step":"retrieve","status":"done",
                  "detail":"Retrieved "+", ".join(d["id"] for d in result["documents"])})
    if bug is None:
        return {"status":"failed","trace":trace,"result":result,"verification":"Unknown issue",
                "verification_run":None,"approval":"Human review required"}
    trace.append({"step":"plan","status":"done","detail":"Select allowlisted check for "+bug["id"]})
    trace.append({"step":"propose","status":"done","detail":bug["fix"]})
    verification=verify_existing_game(bug["id"])
    trace.append({"step":"verify","status":verification["status"],"detail":verification["detail"]})
    trace.append({"step":"report","status":"done","detail":"Report returned; no patch applied."})
    assert len(trace)<=MAX_STEPS
    return {"status":"ready_for_review" if verification["passed"] else "verification_failed",
            "trace":trace,"result":result,"verification":bug["test"],
            "verification_run":verification,"approval":"Human review required; no patch applied"}
