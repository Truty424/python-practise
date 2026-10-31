from typing import TypedDict


class Task(TypedDict):
    id: int
    title: str
    done: bool


def create_task(task_id: int, title: str) -> Task:
    return {
        "id": task_id,
        "title": title,
        "done": False,
    }