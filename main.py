import shelve
import os
import habit
import streak
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

    if args.today:
        user_streak = streak.get_streak()
        due_today = show_todo()
        today = date.today()
        title = "[green]today"
        if not due_today:
            render_obj = f"$ {today.strftime('%a, %d.%b')}\nstreak: {user_streak}\nNo habits due today!"
            render_obj = Text(render_obj)
        else:
            render_obj = f"$ {today.strftime('%a, %d.%b')}\nstreak: {user_streak}\nTo do:\n{pretty_print_habits(due_today)}"
            render_obj = Text(render_obj)
            render_obj.stylize("green")
            print(Panel(render_obj, title_align='left', title=title, expand=False, style="green"))
            choice = Confirm.ask(f"[green]Complete a habit?")
            if choice:
                user_completed = Prompt.ask(f"[green]Complete", choices=[elem.name for elem in due_today])
                with shelve.open("data") as d:
                    data = d[user_completed]
                    data.complete_habit()
                    d[user_completed] = data
    elif args.add:
        h_name = Prompt.ask("[green]Give your habit a name")
        h_freq = IntPrompt.ask(f"[green]How often should your habit <{h_name}> get scheduled? (every _ day(s))")
        habits = retrieve_all()
        tags = [h.tag for h in habits]
        if tags:
            choice = Prompt.ask(f"[green]Add a Tag to group it with other habits or choose from existing tags (Available tags: {tags}",
                            choices=["new", "existing"],
            )
        else:
            choice ="new"
        if choice == "new":
            h_tag = Prompt.ask(f"[green]Add a tag")
        elif choice == "existing":
            h_tag = Prompt.ask(f"[green]Coose a tag", choices=tags)
        confirmation = Confirm.ask(f"[green]Save habit <{h_name}>?")
        if confirmation == False:
            print("[green]Habit discarded")
            return
        new_habit = habit.Habit(h_name, h_tag, h_freq)
        to_file(new_habit)
    elif args.all:
        # TODO: Show next due date for every habit
        habits = retrieve_all()
        render_obj = f"{pretty_print_habits(habits)}"
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
        habits = retrieve_all()
        if not habits:
            print(f"[green]No habits available")
            return
        habit_names = [habit.name for habit in habits]
        name_habit_to_edit = Prompt.ask(f"[green]Choose the habit you want to edit", choices=habit_names)
        field_to_edit = Prompt.ask(f"[green]What do you want to edit", choices=["name", "frequency", "tag"])
        match field_to_edit:
            case "name":
                new_name = Prompt.ask(f"[green]Enter the new name")
                rename(name_habit_to_edit, new_name)
                print(f"[green]Habit renamed to {new_name}")
            case "frequency":
                new_freq = IntPrompt.ask(f"[green]Enter the new frequency (every _ day(s)")
                d = shelve.open("data")
                data = d[name_habit_to_edit]
                data.set_frequency(new_freq) 
                d[name_habit_to_edit] = data
                d.close()
                print(f"[green]Frequency updated!")
            case "tag":
                new_tag = Prompt.ask(f"[green]Enter a new tag")
                d = shelve.open("data")
                data = d[name_habit_to_edit]
                data.tag = new_tag
                d[name_habit_to_edit] = data
                d.close()
                print(f"[green]Tag updated!")
    else:
        today = date.today()
        user_streak = streak.get_streak() 
        render_obj = f"$ {today.strftime('%a, %d.%b')}\nstreak: {user_streak}\ncommands:\n--add: Add a habit\n--delete: Delete a habit\n--today: Show todays to-do's\n--all: Show all habits\n--edit: Edit existing habit"
        title = "[green]dashboard"
        render_obj = Text(render_obj)
    render_obj.stylize("green")
    print(Panel(render_obj, title_align='left', title=title, expand=False, style="green"))


def pretty_print_habits(habits: list) -> str:
    tag_dict = {}
    habits_str = ""
    for h in habits:
        if h.tag not in tag_dict:
            date = h.last_completed + h.frequency
            tag_dict[h.tag] = [f"{h.name} | @due on: {date.strftime('%a, %d.%b')} "]
        else:
            tag_dict[h.tag].append(h.name)
    for key in tag_dict.keys():
        habits_str += "$" + key + ":\n"
        for value in tag_dict[key]:
            habits_str += " >" + value + "\n"
    return habits_str

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
    to_do = [elem for elem in habits if elem.is_due()]
    return to_do

if __name__ == "__main__":
    main()
