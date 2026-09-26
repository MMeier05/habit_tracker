import json
import os

class Habit:
    def __init__(self, name, frequency=1, tag=None):
        self.name = name
        self.frequency = frequency
        self.tag = tag

    def __repr__(self) -> str:
        return f"name: {self.name}, freq: {self.frequency}, tag: {self.tag}"
    


def main():
    for i in range(5):
        name = f"name{i}"
        tag = f"tag{i}"
        habit = Habit(name, i, tag)
        print(habit)
        to_file(habit)


def from_file() -> list[Habit]:
    if not os.path.isfile("habits.json"):
        raise Exception("No file found")
    with open("habits.json", mode="r") as f:
        h_dict = json.load(f)
        print(h_dict)

def to_file(habit: Habit):
    if not os.path.isfile("habits.json"):
        with open("habits.json", "w") as fp:
            pass
    h_dict = {
        "name": habit.name, 
        "frequency": habit.frequency,
        "tag": habit.tag,
    }
    print(h_dict)
    with open("habits.json", "w") as fd:
        json.dump(h_dict, fd) 





if __name__ == "__main__":
    main()
