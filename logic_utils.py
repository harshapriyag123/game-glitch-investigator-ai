"""Core game rules preserved from the completed Module 1 project."""
import random
import re
DIFFICULTIES = {"Easy": (1, 20, 6), "Normal": (1, 100, 8), "Hard": (1, 50, 5)}
def get_range_for_difficulty(difficulty): return DIFFICULTIES[difficulty][:2]
def get_attempt_limit(difficulty): return DIFFICULTIES[difficulty][2]
def parse_guess(raw, low=1, high=100):
    if raw is None or not str(raw).strip(): return False, None, "Enter a guess."
    value = str(raw).strip()
    if not re.fullmatch(r"[+-]?[0-9]+", value): return False, None, "Enter a whole number." if re.search(r"[0-9]", value) else "That is not a number."
    number = int(value)
    if not low <= number <= high: return False, None, f"Enter a whole number from {low} to {high}, including both endpoints."
    return True, number, None
def check_guess(guess, secret):
    if type(guess) is not int or type(secret) is not int: raise TypeError("Guess and secret must be integers.")
    return "Win" if guess == secret else "Too High" if guess > secret else "Too Low"
def get_hint(outcome): return {"Win":"🎉 Correct!", "Too High":"📉 Go LOWER!", "Too Low":"📈 Go HIGHER!"}[outcome]
def update_score(score, outcome, attempt):
    if attempt < 1: raise ValueError("Attempt numbers start at 1.")
    if outcome == "Win": return score + max(10,100-10*(attempt-1))
    if outcome in ("Too High","Too Low"): return score-5
    raise ValueError("Unknown outcome")
def create_game(difficulty):
    low,high=get_range_for_difficulty(difficulty)
    return dict(difficulty=difficulty,secret=random.randint(low,high),attempts=0,score=0,status="playing",history=[],last_outcome=None)
def submit_guess(game,raw):
    if game['status']!='playing': return game,"Game finished. Start a new game to play again."
    low,high=get_range_for_difficulty(game['difficulty'])
    ok,guess,error=parse_guess(raw,low,high)
    if not ok:return game,error
    attempts=game['attempts']+1
    outcome=check_guess(guess,game['secret'])
    status='won' if outcome=='Win' else 'lost' if attempts>=get_attempt_limit(game['difficulty']) else 'playing'
    return {**game,'attempts':attempts,'score':update_score(game['score'],outcome,attempts),'status':status,'history':[*game['history'],guess],'last_outcome':outcome},None
