"""Schema-constrained specialist report, with honest baseline comparison."""
from knowledge import BUGS
from debug_engine import explain_enhanced
ISSUES={bug["id"]:bug for bug in BUGS}
FIELDS=("category","root_cause","evidence","recommended_fix","verification_test","limitations")
def specialized_report(query):
    answer=explain_enhanced(query,use_llm=False)
    if answer["status"]!="ok":
        return {"status":answer["status"],"fields":None,"answer":answer}
    issue=ISSUES[answer["source"]]
    fields={"category":issue["title"],"root_cause":issue["cause"],
            "evidence":[{"id":d["id"],"title":d["title"],"url":d["url"]} for d in answer["documents"]],
            "recommended_fix":issue["fix"],"verification_test":issue["test"],
            "limitations":"Advisory diagnosis of a documented game bug; verify independently before applying fixes."}
    return {"status":"ok","fields":fields,"answer":answer}
def schema_comparison(queries):
    """Measure machine-readable required-field coverage; NOT factual correctness."""
    results=[]
    for query in queries:
        specialist=specialized_report(query)
        obj=specialist.get("fields") or {}
        coverage=sum(bool(obj.get(field)) for field in FIELDS)
        baseline=explain_enhanced(query,use_llm=False)
        # Baseline returns freeform prose, not a top-level six-field structured contract.
        baseline_schema_coverage=sum(bool(baseline.get(field)) for field in FIELDS)
        results.append({"query":query,"baseline_fields":baseline_schema_coverage,
                        "specialized_fields":coverage,"total_fields":len(FIELDS),
                        "status":specialist["status"]})
    return results
