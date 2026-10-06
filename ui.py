from rich.console import Console, Group
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box
from datetime import date, timedelta
import time
import streak
import habit

habit1 = habit.Habit("habit1", 1)
habit2 = habit.Habit("arbeit", 2)
habits_list = [habit1, habit2]

def make_cal_table(habits: list, columns=3) -> Table:
    # TODO: When habit wasnt completed it doesnt show the habits frequency but that its due everyday
    # TODO: Correct behaviour: it should show its due on my_date and then display the correct frequency after
    # TODO: If it isnt completed on my_date and the next date comes, behaviour from above should be repeated until its completed
    
    # TODO: Show on my_date completed habits with a checkmark [✓] and to be completed with [ ] 
    my_date = date.today()
    table_columns = []
    table_rows = []

    #create weekday columns
    for day in range(columns):
        calc_date = my_date + timedelta(day)
        if calc_date == my_date:
            table_columns.append(f"[green blink]*{calc_date.strftime("%A")}")
        else:
            table_columns.append(calc_date.strftime("%A"))

    #create rows
    for habit in habits:
        row = []
        if habit.is_due(date=calc_date):
            row.append(habit.name)
        for day in range(columns - 1):
            calc_date = my_date + timedelta(day)
            if calc_date == my_date + habit.frequency:
                row.append(habit.name)
            else:
                row.append("/")
        table_rows.append(row)

    table = Table(*table_columns, highlight=True, box=None, padding=(0,1))
    for row in table_rows:
        table.add_row(*row)
    return table


class Dashboard:
    # TODO: Show a progress bar of how many habits are left to complete with a [completed / all today] box after, the streak should only increment once the user completed all habits (maybe configurable to a percentage)
    def __init__(self, habits: list):
        self.habits = habits

    def __rich__(self) -> Panel:
        user_streak = streak.get_streak() 
        cur_date = date.today().strftime('%a, %d.%b')
        

        panel = Panel(
            Align.left(
                Group(
                    Text(f"{cur_date}"),
                    Text(f"{user_streak} days", style="green"),
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
            make_cal_table(self.habits),
            title_align='left', 
            title="[green]$ [bold]calendar",
            expand=False,
            padding=(0, 4),
            border_style="yellow",
        )
        return panel

console = Console()
dashboard = Dashboard(habits_list)
calendar = Calendar(habits_list)

console.print(dashboard, calendar)



