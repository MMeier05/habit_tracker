import time
import datetime as dt
import streak

class Habit:
    def __init__(self, name, tag=None, frequency=1):
        self.name: str = name
        self.tag: str = tag
        self.frequency: timedelta = dt.timedelta(frequency)
        self.created: datetime = dt.date.today()
        self.last_completed: datetime = self.created
        

    def __repr__(self) -> str:
        return f"""
Habit obj: {self.name}(
freq: {self.frequency},
tag: {self.tag},
created: {self.created},
last_completed: {self.last_completed})"""

    def is_due(self) -> bool:
        cur_time = dt.date.today()
        return True if  (cur_time - self.last_completed) >= self.frequency else False

    def complete_habit(self):
        if not self.is_due():
            raise Exception("Habit not overdue")
        else:
            self.last_completed = dt.date.today()
            streak.increment()

    def set_frequency(self, new_freq):
        self.frequency = dt.timedelta(new_freq)



