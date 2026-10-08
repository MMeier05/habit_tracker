from rich.console import Console
from rich import print
import typer
import datetime as dt
from ui import Dashboard, Calendar
import habit as h
import streak as s
from typing import Annotated

app = typer.Typer()
console = Console()
h_list = h.show_todo()
s.check_for_reset()

def interval_callback(value: int):
    if value and value <= 0:
        raise typer.BadParameter("The interval must be bigger than 0 days.")
    return value

@app.command()
def cal(size: Annotated[int, typer.Option(help="Size of the printed calendar.")] = 4) :
    """
    Prints the calendar
    """
    console.print(Calendar(h_list, size))

@app.callback(invoke_without_command=True)
@app.command()
def dash(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print(Dashboard(h_list))

@app.command()
def add(
    name: Annotated[str, typer.Argument(help="The name of your habit.")],
    interval: Annotated[int, typer.Argument(
        help="The interval your habit gets scheduled.",
        callback=interval_callback,
    )] = 1
):
    """
    Add new habits
    """
    hab = h.Habit(name, interval)
    h.to_file(hab)
    i_string = f"{interval} days" if interval > 1 else f"day"
    console.print(f"[green bold][magenta]{name}[/magenta] was added and gets scheduled every {i_string}!")

@app.command()
def rm(name: Annotated[str, typer.Argument(help="Name of the to be deleted habit.")]):
    """
    Delete habits
    """
    if h.remove(name):
        console.print(f"[green][italic]Success[/italic]\n[magenta]{name}[/magenta] was removed!")
    else:
        raise typer.BadParameter(f"{name} does not exist!")

@app.command()
def edit(
    habit_name: Annotated[str, typer.Argument(help="The name of the to be edited habit.")],
    name: Annotated[str, typer.Option(help="Edit the name.")] = None,
    schedule: Annotated[int, typer.Option(
        help="Edit the habits schedule.",
        callback=interval_callback,
    )] = None,
):
    """
    Edit existing habits
    """
    console.print(f"[green][italic]Success[/italic]")
    if name:
        if not h.edit_name(habit_name, name):
            raise typer.BadParameter(f"{habit_name} does not exist!")
        console.print(f"[magenta]{habit_name} [green]-> [magenta]{name}")
        habit_name = name
    if schedule:
        if not h.edit_schedule(habit_name, schedule):
            raise typer.BadParameter(f"{habit_name} does not exist!")
        i_string = f"[magenta]{schedule} [green]days" if schedule > 1 else f"[green]day"
        console.print(f"[green]Scheduled every {i_string}")

@app.command()
def done(name: Annotated[str, typer.Argument(help="The name of the habit.")]):
    """
    Complete habits
    """
    if not h.complete_habit(name):
        raise typer.BadParameter(f"{name} does not exist!")
    console.print(f"[green]Completed [magenta]{name}")
    still_to_do = list(filter(lambda x: x.is_due(), h.show_todo()))
    if not still_to_do:
        s.increment()


if __name__ == "__main__":
    app()
