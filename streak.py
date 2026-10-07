import shelve
import datetime as dt

def get() -> int:
    with shelve.open("streak_data") as d:
        if "streak" in d:
            return d["streak"]
        else:
            return 0 

def increment():
    """
    Only increment when all completed
    """
    with shelve.open("streak_data") as d:
        key = str(dt.date.today())
        if "streak" not in d:
            d["streak"] = 1
            d[key] = True
            yesterday = str(dt.date.today() - dt.timedelta(1))
            d[yesterday] = True
        if key not in d:
            print("This should print")
            d[key] = True
            d["streak"] += 1
            print("Now streak was inc")
        d.close()

def reset():
    with shelve.open("streak_data") as d:
        if "streak" in d:
            d["streak"] = 0  

def check_for_reset():
    yesterday = str(dt.date.today() - dt.timedelta(1))
    with shelve.open("streak_data") as d:
        if yesterday not in d:
            reset()

