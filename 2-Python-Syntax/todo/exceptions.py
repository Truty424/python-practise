class TodoError(Exception):
    pass


class TaskNotFoundError(TodoError):
    pass


class TaskAlreadyDoneError(TodoError):
    pass


class InvalidTaskError(TodoError):
    pass
