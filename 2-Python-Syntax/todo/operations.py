from .tasks import Task, create_task
from .exceptions import TaskNotFoundError, TaskAlreadyDoneError


def add_tasks(tasks: list[Task], title: str) -> Task:
    if not tasks:
        new_id = 1
    else:
        ids = [task["id"] for task in tasks]
        new_id = max(ids) + 1
    new_task = create_task(task_id=new_id, title=title)
    tasks.append(new_task)
    return new_task

def remove_task(tasks: list[Task], task_id: int) -> None:
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise TaskNotFoundError(f"Task with ID #{task_id} not found")

def mark_as_done(tasks: list[Task], task_id: int) -> Task:
    for task in tasks:
        if task["id"] == task_id:
            if not task["done"]:
                task["done"] = True
                return task
            else:
                raise TaskAlreadyDoneError(f"Task with ID #{task_id} already done")
    raise TaskNotFoundError(f"Task with ID #{task_id} not found")
