from rich.console import Console, Group
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box
from datetime import date
import calendar
import time
import streak

def make_cal_table() -> Table:
    my_date = date.today()
    days = []
    for day in range(my_date.weekday(), my_date.weekday() + 3):
        if day == my_date.weekday():
            days.append("[green blink]Today")
        else:
            days.append(calendar.day_name[day])

    table = Table(*days, box=box.SIMPLE_HEAD)
    table.add_row("habit1", "/", "/")
    table.add_row("habit2", "/", "/")
    return table


class Dashboard:
    def __rich__(self) -> Panel:
        user_streak = streak.get_streak() 
        cur_date = date.today().strftime('%a, %d.%b')
        


        panel = Panel(
            Align.left(
                Group(
                    Text(f"{cur_date}"),
                    Text(f"{user_streak} days", style="green"),
                    make_cal_table(),
                )
            ),
            title_align='left', 
            title="[green]$ [bold]dashboard",
            border_style="grey58",
            expand=False,
            padding=(0, 3),

        )
        return panel

table = make_cal_table()
console = Console()
dashboard = Dashboard()

console.print(dashboard)



