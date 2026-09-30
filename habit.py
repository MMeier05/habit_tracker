import time
import datetime as dt

class Habit:
    def __init__(self, name, tag=None, frequency=1):
        self.name: str = name
        self.tag: str = tag
        self.frequency: timedelta = dt.timedelta(frequency)
        self.created: datetime = get_time()
        self.last_completed: datetime = self.created
        

    def __repr__(self) -> str:
        return f"""
Habit obj: {self.name}(
freq: {self.frequency},
tag: {self.tag},
created: {self.created},
last_completed: {self.last_completed})"""

    def is_due(self) -> bool:
        cur_time = get_time()
        return True if  (cur_time - self.last_completed) >= self.frequency else False

    def complete_habit(self):
        if not self.is_overdue():
            raise Exception("Habit not overdue")
        else:
            self.last_completed = get_time()


def get_time() -> datetime:
    time_s = time.localtime()
    return dt.datetime(time_s.tm_year, time_s.tm_mon, time_s.tm_mday)
