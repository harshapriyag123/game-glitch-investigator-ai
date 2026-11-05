"""Allowlisted, read-only tests of current game invariants—not arbitrary user code."""
from logic_utils import check_guess,create_game,parse_guess,submit_guess
def _check_comparison():
    return check_guess(4,53)=="Too Low" and check_guess(53,4)=="Too High"
def _check_session():
    game=create_game("Easy")
    guess=1 if game["secret"]!=1 else 2
    updated,error=submit_guess(game,str(guess))
    return error is None and updated["secret"]==game["secret"] and updated["attempts"]==1
def _check_validation():
    game=create_game("Easy")
    for invalid in ("","abc","17.5","21"):
        new,error=submit_guess(game,invalid)
        if not error or new!=game:return False
    return True
def _check_limits():
    return (parse_guess("1",1,20)[0] and parse_guess("20",1,20)[0] 
            and not parse_guess("0",1,20)[0] and not parse_guess("21",1,20)[0])
def _check_restart():
    fresh=create_game("Normal")
    return fresh["attempts"]==0 and fresh["score"]==0 and fresh["history"]==[] and fresh["status"]=="playing"
TOOLS={"numeric_comparison":_check_comparison,"secret_reset":_check_session,
       "invalid_attempt":_check_validation,"difficulty_bounds":_check_limits,
       "game_restart":_check_restart}
def verify_existing_game(issue_id):
    """Run only predefined, safe tests on current code; never execute a submitted snippet."""
    check=TOOLS.get(issue_id)
    if check is None:return {"status":"unsupported","passed":False,"detail":"No allowlisted check for this issue"}
    try:
        passed=bool(check())
        return {"status":"passed" if passed else "failed","passed":passed,
                "detail":"Predefined check of existing game behavior; this does not test a proposed patch."}
    except Exception as exc:
        return {"status":"error","passed":False,"detail":"Verification error: "+type(exc).__name__}
