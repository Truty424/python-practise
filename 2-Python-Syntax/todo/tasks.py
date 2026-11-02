from typing import TypedDict


class Task(TypedDict):
    id: int
    title: str
    done: bool


def create_task(task_id: int, title: str) -> Task:
    if type(task_id) is not int:
        raise TypeError("Task id must be an integer")

    if task_id <= 0:
        raise ValueError("Task id must be greater than zero")

    if not isinstance(title, str):
        raise TypeError("Title must be a string")

    if not title.strip():
        raise ValueError("Title cannot be empty")

    return {
        "id": task_id,
        "title": title,
        "done": False,
    }
