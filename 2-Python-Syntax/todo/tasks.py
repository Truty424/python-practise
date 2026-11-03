from typing import TypedDict

from .exceptions import InvalidTaskError


class Task(TypedDict):
    id: int
    title: str
    done: bool


def create_task(task_id: int, title: str) -> Task:
    if task_id <= 0:
        raise InvalidTaskError("Task id must be greater than zero")

    if not title.strip():
        raise InvalidTaskError("Title cannot be empty")

    return {
        "id": task_id,
        "title": title,
        "done": False,
    }
