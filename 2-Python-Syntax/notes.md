# 1. Built-in Types & Mutability

## Built-in Types

| Type | Example | Mutable |
|---|---|---|
| `int` | `10` | No |
| `float` | `3.14` | No |
| `str` | `"Hello"` | No |
| `bool` | `True` | No |
| `list` | `[1, 2, 3]` | Yes |
| `tuple` | `(1, 2, 3)` | No |
| `dict` | `{"a": 1}` | Yes |
| `set` | `{1, 2, 3}` | Yes |
| `NoneType` | `None` | No |

## Mutable vs Immutable

- **Mutable:** An object can be modified after creation (`list`, `dict`, `set`).
- **Immutable:** An object cannot be modified after creation (`int`, `str`, `tuple`).

### References vs Copies

```python
a = [1, 2, 3]
b = a             # Same object
b.append(4)
print(a)          # [1, 2, 3, 4]
```

### Copying a List

```python
a = [1, 2, 3]
b = a.copy()      # Shallow copy
b.append(4)

print(a)          # [1, 2, 3]
print(b)          # [1, 2, 3, 4]
```

**Remember:**
- `b = a` — both variables reference the same object.
- `b = a.copy()` — creates a new list (shallow copy).
- `list` is mutable, while `str` and `tuple` are immutable.
- A shallow copy does not duplicate nested mutable objects.
# 2. Comprehensions

Comprehensions provide a concise way to create collections from iterables.

### List Comprehension

```python
squares = [x ** 2 for x in range(5)]
# [0, 1, 4, 9, 16]
```

### Filtering with `if`

```python
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]
```

### Conditional Expression (`if/else`)

```python
labels = ["even" if x % 2 == 0 else "odd" for x in range(3)]
# ["even", "odd", "even"]
```

### Dict Comprehension

```python
squares = {x: x ** 2 for x in range(4)}
# {0: 0, 1: 1, 2: 4, 3: 9}
```

### Set Comprehension

```python
unique = {abs(x) for x in [-2, 2, -3, 3]}
# {2, 3}
```

**Remember:**
- `[expression for x in iterable]` → list
- `{key: value for x in iterable}` → dict
- `{expression for x in iterable}` → set
- `if` after `for` filters elements.
- `if/else` before `for` transforms elements conditionally.
- Prefer regular loops when comprehensions become difficult to read.

# 3. Functions 

## `*args` — Positional Arguments

Accepts any number of positional arguments as a tuple.

```python
def multiply(*args):
    result = 1
    for number in args:
        result *= number
    return result

multiply(2, 3, 4)  # 24
```

## `**kwargs` — Keyword Arguments

Accepts any number of keyword arguments as a dictionary.

```python
def print_user(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_user(name="Adam", age=25)
```

## Default Arguments

Parameters can have default values.

```python
def create_user(name, role="user"):
    return {"name": name, "role": role}
```

## Mutable Default Argument Trap

Mutable default arguments are evaluated once when the function is defined, not on every call.

**Avoid:**

```python
def add_item(item, items=[]):
    items.append(item)
    return items
```

**Prefer:**

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

## Lambda Functions

Anonymous functions containing a single expression.

```python
square = lambda x: x ** 2

numbers = [5, 2, 9, 1]
sorted(numbers, key=lambda x: abs(x - 5))
```

Often used with `sorted()`, `map()` and `filter()`.

**Remember:**
- `*args` → tuple of positional arguments.
- `**kwargs` → dict of keyword arguments.
- Default arguments make parameters optional.
- Avoid mutable defaults unless shared state is intentional.
- `lambda` automatically returns its expression.
- Prefer `def` for named or more complex functions.

# 4. Type Hints & mypy Cheat Sheet

### Type Hints

Specify expected parameter and return types.

```python
def multiply(x: int, y: int) -> int:
    return x * y
```

### Optional & Union

```python
name: str | None = None   # str or None
value: int | str = 10     # int or str
```

- `Optional[str]` = `str | None`
- `Union[int, str]` = `int | str`
- `Optional` does not make a parameter optional to pass — a default value does.

### Generics — Collections

```python
numbers: list[int] = [1, 2, 3]
names: set[str] = {"Adam", "Anna"}
ages: dict[str, int] = {"Adam": 25}
person: tuple[str, int] = ("Adam", 25)
```

### TypedDict

Defines the expected keys and value types of a dictionary.

```python
from typing import TypedDict

class Product(TypedDict):
    name: str
    price: float
    available: bool
```

### mypy — Static Type Checking

```bash
uv add --dev mypy
uv run mypy 2-Python-Syntax/type_hints.py
```

**Remember:**
- Type hints are not enforced automatically at runtime.
- `mypy` detects type inconsistencies without executing code.
- `-> None` means a function does not return a useful value.
- `list[str | int]` means a list containing strings or integers.
- `dict[K, V]` accepts exactly two type arguments: key and value types.
- `TypedDict` describes dictionary structure but does not validate data at runtime.

#  5. Modules, Packages & Imports 

## Modules & Packages

- **Module** — a single `.py` file containing Python code.
- **Package** — a directory grouping related modules.
- `__init__.py` — marks a regular package; can be empty or expose selected functions.
- `__main__.py` — entry point when running a package with `python -m`.

## Imports

```python
import math_utils
from math_utils import add
import math_utils as mu

# Relative import (inside a package)
from .operations import add

# Absolute import
from calculator.operations import add
```

- **Absolute import** — uses the full package path.
- **Relative import** — uses `.` for the current package.
- Avoid `from module import *`.

## `if __name__ == "__main__"`

```python
def main() -> None:
    print("Hello!")

if __name__ == "__main__":
    main()
```

- Direct execution → `__name__ == "__main__"`.
- Import → `__name__` is the module name.
- Prevents code inside the condition from running during import.

## Running Packages

```text
calculator/
├── __init__.py
├── __main__.py
└── operations.py
```

```bash
python -m calculator
```

Executes `calculator/__main__.py`.

## Circular Imports

Occur when modules import each other.

```python
# a.py
from b import function_b

# b.py
from a import function_a
```

- Can cause `ImportError` due to partially initialized modules.
- **Solution:** Move shared functionality to a separate module or restructure dependencies.

**Remember:**
- Module = file; package = collection of modules.
- `__init__.py` initializes a regular package.
- `__main__.py` enables package execution with `-m`.
- Prefer explicit imports.
- Avoid circular dependencies.

# 6. Exceptions 

## try / except / else / finally

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
else:
    print(result)
finally:
    print("Finished")
```

- `try` — executes code that may raise an exception.
- `except` — handles a matching exception.
- `else` — runs if `try` completes without exceptions.
- `finally` — runs regardless of success or failure (under normal execution).

## Common Exceptions

| Exception | Description |
|---|---|
| `ValueError` | Invalid value |
| `TypeError` | Invalid type or operation |
| `ZeroDivisionError` | Division by zero |
| `IndexError` | Invalid list index |
| `KeyError` | Missing dictionary key |
| `FileNotFoundError` | File does not exist |
| `ImportError` | Import failure |

## raise — Raising Exceptions

```python
def validate_age(age: int) -> bool:
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age >= 18
```

`raise` explicitly raises an exception.

## Custom Exceptions

Create application-specific exceptions by inheriting from `Exception`.

```python
class TaskNotFoundError(Exception):
    pass


def remove_task(task_id: int) -> None:
    raise TaskNotFoundError(f"Task {task_id} not found")
```

## Exception Hierarchy

```text
BaseException
└── Exception
    ├── ValueError
    ├── TypeError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    └── OSError
        └── FileNotFoundError
```

## Remember

- Catch **specific exceptions** instead of using bare `except:`.
- Use `raise` to signal invalid operations.
- Use custom exceptions for application-specific errors.
- Use `else` for code that should run only when `try` succeeds.
- Use `finally` for cleanup operations.
- Prefer `with open(...)` for automatic file management.
- Unhandled exceptions propagate up the call stack and may terminate the program.

# 7. f-strings & Formatting 

## f-strings — Basics

Insert variables and expressions directly into strings.

```python
name = "Adam"
age = 25

print(f"Name: {name}, Age: {age}")
print(f"Next year: {age + 1}")
```

## Number Formatting

```python
price = 1234.567
discount = 0.155

f"{price:.2f}"      # 1234.57
f"{price:,.2f}"     # 1,234.57
f"{discount:.1%}"   # 15.5%
```

- `.2f` — 2 decimal places.
- `,` — thousands separator.
- `.1%` — percentage with 1 decimal place.

## Text Alignment

```python
name = "Python"

f"{name:<10}"  # Left-aligned
f"{name:>10}"  # Right-aligned
f"{name:^10}"  # Centered
```

`10` specifies the minimum field width.

## Date Formatting

```python
from datetime import datetime

now = datetime.now()

f"{now:%Y-%m-%d}"        # 2026-11-02
f"{now:%d/%m/%Y %H:%M}"  # Date and time
```

Common directives: `%Y` (year), `%m` (month), `%d` (day), `%H` (hour), `%M` (minute), `%S` (second).

## Useful Features

```python
x = 10

f"{x=}"     # x=10 (debugging)
f"{x!r}"    # 10 (repr)
f"{{x}}"    # {x} (literal braces)
```

Conditional formatting:

```python
done = True
f"{'Done' if done else 'Pending'}"  # Done
```

## Other Formatting Methods

```python
"Hello, {}".format(name)  # str.format()
"Hello, %s" % name        # Old %-formatting
```

**Remember:**
- Prefer f-strings for readable string formatting.
- Use `:.2f` for decimal precision and `:.1%` for percentages.
- Use `<`, `>` and `^` for alignment.
- Use `!r` and `=` for debugging.
- Use `{{` and `}}` to display literal braces.

# 8. Virtualenv vs Global Interpreter

## Global Interpreter vs Virtual Environment

- **Global interpreter** — Python installation available outside a project's virtual environment.
- **Virtual environment (`venv`)** — an isolated environment with its own installed packages.
- Different projects can use different dependency versions without conflicts.
- A virtual environment usually references a base Python installation rather than copying the entire interpreter.

## Why Use Virtual Environments?

- **Dependency isolation** — prevents version conflicts between projects.
- **Reproducibility** — makes it easier to recreate consistent environments.
- **Safety** — avoids modifying global or system Python packages.
- **Portability** — allows projects to use different Python versions and dependencies.

## Interpreter vs Environment

- **Interpreter** — executes Python code.
- **Environment** — determines which interpreter and installed packages are used.
- Activating a `venv` changes which Python executable is found through `PATH`.
- Type hints and Python syntax behavior depend on the interpreter version, not on the virtual environment itself.

**Remember:** Use a separate virtual environment for each project to isolate dependencies and avoid conflicts.