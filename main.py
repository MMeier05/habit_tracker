import shelve
import os
import habit
import argparse
from datetime import date
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.prompt import Prompt, IntPrompt, Confirm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--today', help="show todays tasks", action="store_true")
    parser.add_argument('--add', help="add to-do", action="store_true")
    parser.add_argument('--all', help="show all habits", action="store_true")
    parser.add_argument('--delete', help="delete a habit", action="store_true")
    parser.add_argument('--edit', help="edit habit", action="store_true")
    args = parser.parse_args()
    
    today = date.today()
    render_obj = f"$ {today}\ncommands:\n--add: Add a habit\n--delete: Delete a habit\n--today: Show todays to-do's\n--all: Show all habits"
    title = "[green]dashboard"
    render_obj = Text(render_obj)

    if args.today:
        due_today = show_todo()
        if not due_today:
            due_today = "No habits available :(\nAdd your first habit with --add!"
            today = date.today()

        render_obj = f"$ {today}\n{due_today}"
        title = "[green]today"
        render_obj = Text(render_obj)
    elif args.add:
        h_name = Prompt.ask("[green]Give your habit a name")
        h_freq = IntPrompt.ask(f"[green]How often should your habit <{h_name}> get scheduled? (every _ day(s))")
        # TODO: Show option of available tags or add new tag
        h_tag = Prompt.ask(f"[green]Add a Tag to group it with other habits")
        confirmation = Confirm.ask(f"[green]Save habit <{h_name}>?")
        habit1 = habit.Habit(h_name, h_tag, h_freq)
        to_file(habit1)
    elif args.all:
        habits = retrieve_all()
        render_obj = f"$ {habits}"
        title = "[green]all habits"
        render_obj = Text(render_obj)
    elif args.delete:
        habits = retrieve_all()
        if not habits:
            print(f"[green]No habits available")
        else:
            names = [habit.name for habit in habits]
            h_name = Prompt.ask(f"[green]Enter the name of the habit you want to delete", choices=names)
            if remove(h_name):
                print(f"[green]Successfully removed <{h_name}>")
            else:
                print(f"[green]Error removing <{h_name}>")
    elif args.edit:
        pass

    else:
        pass

    render_obj.stylize("green")
    print(Panel(render_obj, title_align='left', title=title, expand=False, style="green"))
    


#def from_file() -> list[Habit]:
#    if not os.path.isfile("data.pickle"):
#        raise Exception("No file found")
#    with open("data.pickle", mode="rb+") as f:
#        data_list = []
#        try:
#            while True:
#                data_list.append(pickle.load(f))
#        except EOFError:
#            pass
#    return data_list


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

def retrieve_all() -> list[Habit]:
    d = shelve.open("data")
    data_list = [d[key] for key in list(d.keys())]
    d.close()
    return data_list

def to_file(habit: Habit):
    d = shelve.open("data")
    d[habit.name] = habit
    d.close()

def show_todo() -> list[Habit]:
    habits = retrieve_all()
    to_do = []
    if not to_do:
        return None
    for elem in habits:
        if elem.is_overdue():
            to_do.append(elem)
    return to_do

if __name__ == "__main__":
    main()
