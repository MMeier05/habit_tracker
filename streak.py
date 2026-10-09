import shelve
import datetime as dt
from pathlib import Path

DATA_DIR = Path.home() /".habit_tracker"
DATA_DIR.mkdir(exist_ok=True)
STREAK_PATH = str(DATA_DIR / "streak_data")

def get() -> int:
    with shelve.open(STREAK_PATH) as d:
        if "streak" in d:
            return d["streak"]
        else:
            return 0 

def increment():
    """
    Only increment when all completed
    """
    with shelve.open(STREAK_PATH) as d:
        key = str(dt.date.today())
        if "streak" not in d:
            d["streak"] = 1
            d[key] = True
            yesterday = str(dt.date.today() - dt.timedelta(1))
            d[yesterday] = True
        if key not in d:
            d[key] = True
            d["streak"] += 1
        d.close()

def reset():
    with shelve.open(STREAK_PATH) as d:
        if "streak" in d:
            d["streak"] = 0  

def check_for_reset():
    yesterday = str(dt.date.today() - dt.timedelta(1))
    with shelve.open(STREAK_PATH) as d:
        if yesterday not in d:
            reset()

