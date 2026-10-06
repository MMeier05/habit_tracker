import time
import shelve
import datetime as dt
import streak

class Habit:
    def __init__(self, name, frequency):
        self.name: str = name
        self.frequency: timedelta = dt.timedelta(frequency)
        self.created: datetime = dt.date.today()
        self.last_completed: datetime = dt.date(1, 1, 1)


    def __repr__(self) -> str:
        return f"""
Habit obj: {self.name}(
freq: {self.frequency},
tag: {self.tag},
created: {self.created},
last_completed: {self.last_completed})"""

    def is_due(self, date="today") -> bool:
        if date == "today":
            cur_time = dt.date.today()
        elif isinstance(date, dt.date):
            cur_time = date
        else:
            raise Exception("Date must either be 'today' or valid datetime.date format")

        return True if (self.last_completed + self.frequency) <= cur_time else False

    def complete(self):
        if not self.is_due():
            raise Exception("Habit not overdue")
        else:
            self.last_completed = dt.date.today()

    def set_frequency(self, new_freq):
        self.frequency = dt.timedelta(new_freq)


def remove(habit: str) -> bool:
    d = shelve.open("data")
    if habit in d:
        del d[habit]
        d.close()
        return True
    d.close()
    return False

def rename(habit: str, new_name: str) -> Habit | None:
    d = shelve.open("data")
    if habit in d:
        data = d[habit]
        del d[habit]
    else:
        return None
    data.name = new_name
    d[new_name] = data
    d.close()
    return data

def to_file(habit: Habit):
    d = shelve.open("data")
    d[habit.name] = habit
    d.close()

def retrieve_all() -> list[Habit]:
    d = shelve.open("data")
    data_list = [d[key] for key in list(d.keys())]
    d.close()
    return data_list

def show_todo() -> list[tuple[bool, Habit]]:
    habits = retrieve_all()
    to_do = [elem for elem in habits if elem.is_due() or elem.last_completed == dt.date.today()]
    return to_do
