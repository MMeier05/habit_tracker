from rich.console import Console, Group
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.progress_bar import ProgressBar
from rich.bar import Bar
from rich import box
from datetime import date, timedelta
import time
import streak
import habit

habit1 = habit.Habit("habit1", 2)
habit1.complete()
habit2 = habit.Habit("arbeit", 1)
habits_list = [habit1, habit2]

def make_cal_table(habits: list, columns=3) -> Table:
    my_date = date.today()
    table_columns = []
    table_rows = []

    #create weekday columns
    for day in range(columns):
        calc_date = my_date + timedelta(day)
        if calc_date == my_date:
            table_columns.append(f"[magenta blink]*{calc_date.strftime("%A")}")
        else:
            table_columns.append(calc_date.strftime("%A"))

    #create rows
    for habit in habits:
        row = []
        if habit.last_completed == my_date:
            row.append(f"[green][✓]{habit.name}")
        else:
            row.append(f"[ ]{habit.name}")
        for day in range(columns - 1):
            calc_date = my_date + timedelta(day)
            if calc_date.day % habit.frequency.days == 0:
                row.append(habit.name)
            else:
                row.append("/")
        table_rows.append(row)

    table = Table(*table_columns, highlight=True, box=None, padding=(0,1))
    for row in table_rows:
        table.add_row(*row)
    return table

def make_progress_bar(habits: list):
    size = len(habits)
    steps = len([habit for habit in habits if not habit.is_due()])
    grid = Table.grid()
    grid.add_row(
        Bar(size, begin=0, end=steps, width=12, color="green", bgcolor="grey89"),
        Text(f" {int((steps / size) * 100)}% ", style="green"),
        Text(f"[{steps}/{size}]"),
    )
    return grid

class Dashboard:
    def __init__(self, habits: list):
        self.habits = habits

    def __rich__(self) -> Panel:
        user_streak = streak.get_streak() 
        cur_date = date.today().strftime('%a, %d.%b')
        

        panel = Panel(
            Align.left(
                Group(
                    Text(f"@{cur_date}"),
                    Text(f"{user_streak} days", style="green"),
                    make_progress_bar(self.habits),
                )
            ),
            title_align='left', 
            title="[green]$ [bold]dashboard",
            expand=False,
            padding=(0, 4),
            border_style="yellow",
        )
        return panel

class Calendar:
    def __init__(self, habits: list):
        self.habits = habits

    def __rich__(self) -> Panel:
        panel = Panel(
            make_cal_table(self.habits, 4),
            title_align='left', 
            title="[green]$ [bold]calendar",
            expand=False,
            padding=(0, 4),
            border_style="yellow",
        )
        return panel

console = Console()
calendar = Calendar(habits_list)
dashboard = Dashboard(habits_list)

console.print(dashboard, calendar)



