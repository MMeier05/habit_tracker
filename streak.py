import shelve

def get_streak() -> int:
    with shelve.open("streak_data") as d:
        if "streak" in d:
            return d["streak"]
        else:
            return 0 

def increment():
    with shelve.open("streak_data") as d:
        if "streak" in d:
            d["streak"] += 1 
        else:
            d["streak"] = 1 

def reset_streak():
    with shelve.open("streak_data") as d:
        if "streak" in d:
            d["streak"] = 0

