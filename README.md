# CLI Habit Tracker

With this Python command-line tool you can create habits complete them and build a streak.

## Usage

```bash
habit <command>
```

Commands Available:

* `add <name> <interval>`: Add a habit with a specified interval in days (default is 1).
* `edit <old_name> --name <new_name> --schedule <new_schedule>`: Edit the name or schedule of a habit.
* `rm <name>`: Remove the specified habit.
* `done <name>` : Complete the habit for the day.
* `cal --size <size>`: Print the calendar with an optional size.
* `dash`: Print the dashboard
* `--help`: Show the help

## Installation

Requires [uv](https://docs.astral.sh/uv/).

Install directly from GitHub:

```bash
uv tool install git+https://github.com/MMeier05/habit_tracker
```

Or clone and install locally:

```bash
git clone https://github.com/MMeier05/habit_tracker.git
cd habit_tracker
uv tool install . 
```

To uninstall:

```bash
uv tool uninstall habit_tracker
```
