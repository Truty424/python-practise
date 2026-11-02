import argparse
from pathlib import Path

from .exceptions import TaskAlreadyDoneError, TaskNotFoundError
from .operations import add_tasks, mark_as_done, remove_task
from .storage import load_tasks, save_tasks

TASKS_FILE = Path("tasks.json")


def main() -> None:
    parser = argparse.ArgumentParser(description="TODO CLI application")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="Task ID")

    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()
    if args.command == "add":
        tasks = load_tasks(TASKS_FILE)
        try:
            new_task = add_tasks(tasks, args.title)
        except ValueError as error:
            print(f"Error: {error}")
            return
        else:
            save_tasks(TASKS_FILE, tasks)
            print(f"Added task #{new_task['id']}: {new_task['title']}")

    elif args.command == "list":
        tasks = load_tasks(TASKS_FILE)

        if tasks:
            print(f"{'ID':<4} | {'TITLE':<25} | DONE")
            print("-" * 40)

            for task in tasks:
                status = "[x]" if task["done"] else "[ ]"
                print(f"{task['id']:<4} | {task['title']:<25} | {status}")
        else:
            print("No tasks found")

    elif args.command == "done":
        tasks = load_tasks(TASKS_FILE)
        try:
            done_task = mark_as_done(tasks, args.id)
        except (TaskNotFoundError, TaskAlreadyDoneError) as error:
            print(f"Error: {error}")
            return
        else:
            save_tasks(TASKS_FILE, tasks)
            print(f"Done: {done_task['title']}")


    elif args.command == "remove":
        tasks = load_tasks(TASKS_FILE)
        try:
            remove_task(tasks, args.id)
        except TaskNotFoundError as error:
            print(f"Error: {error}")
            return
        save_tasks(TASKS_FILE, tasks)
        print(f"Removed task #{args.id}")
