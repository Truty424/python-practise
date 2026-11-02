import json
from pathlib import Path

from .tasks import Task


def load_tasks(file_path: Path) -> list[Task]:
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        tasks: list[Task] = json.load(f)

    return tasks


def save_tasks(file_path: Path, tasks: list[Task]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)
