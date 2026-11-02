from pathlib import Path

import pytest

from todo.exceptions import TaskAlreadyDoneError, TaskNotFoundError
from todo.operations import add_tasks, mark_as_done, remove_task
from todo.storage import load_tasks, save_tasks
from todo.tasks import Task, create_task


def test_create_task() -> None:
    task = create_task(1, "Learn Python")

    assert task["id"] == 1
    assert task["title"] == "Learn Python"
    assert task["done"] is False


def test_add_tasks() -> None:
    tasks: list[Task] = []

    task1 = add_tasks(tasks, "Learn Python")
    task2 = add_tasks(tasks, "Learn Git")

    assert task1["id"] == 1
    assert task1["title"] == "Learn Python"
    assert task1["done"] is False

    assert task2["id"] == 2
    assert task2["title"] == "Learn Git"
    assert task2["done"] is False

    assert len(tasks) == 2


def test_remove_task() -> None:
    tasks: list[Task] = []
    add_tasks(tasks, "Learn Python")
    add_tasks(tasks, "Learn Git")

    remove_task(tasks, 2)

    assert tasks[0]["id"] == 1
    assert tasks[0]["title"] == "Learn Python"
    assert len(tasks) == 1


def test_remove_nonexistent_task() -> None:
    tasks: list[Task] = []

    with pytest.raises(TaskNotFoundError):
        remove_task(tasks, 1)


def test_mark_as_done() -> None:
    tasks: list[Task] = []
    add_tasks(tasks, "Learn Python")

    mark_as_done(tasks, 1)
    assert tasks[0]["title"] == "Learn Python"
    assert tasks[0]["done"] is True


def test_mark_already_done() -> None:
    tasks: list[Task] = []

    add_tasks(tasks, "Learn Python")
    mark_as_done(tasks, 1)

    with pytest.raises(TaskAlreadyDoneError):
        mark_as_done(tasks, 1)


def test_mark_nonexistent_task_as_done() -> None:
    tasks: list[Task] = []

    with pytest.raises(TaskNotFoundError):
        mark_as_done(tasks, 1)


def test_save_and_load_tasks(tmp_path: Path) -> None:
    file_path = tmp_path / "tasks.json"
    tasks: list[Task] = []

    add_tasks(tasks, "Learn Python")
    add_tasks(tasks, "Learn Git")

    save_tasks(file_path, tasks)
    loaded_tasks = load_tasks(file_path)

    assert len(loaded_tasks) == 2
    assert loaded_tasks[0]["title"] == "Learn Python"
    assert loaded_tasks[1]["title"] == "Learn Git"
    assert loaded_tasks[0]["done"] is False
    assert loaded_tasks[1]["done"] is False


def test_load_tasks_returns_empty_list_when_file_does_not_exist(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.json"

    loaded_tasks = load_tasks(file_path)

    assert loaded_tasks == []
