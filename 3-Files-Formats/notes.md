# 1. File Handling

- `open(path, mode, encoding="utf-8")` — opens a file.
- `r` — read; `w` — overwrite; `a` — append; `b` — binary mode.
- `with` — automatically closes the file, even if an exception occurs.
- `read()` — reads the entire file into memory.
- `readline()` — reads one line.
- `for line in file` — memory-efficient line-by-line reading.
- `write()` — writes text to a file; `\n` adds a new line.
- `strip()` — removes leading and trailing whitespace.
- `enumerate(file, start=1)` — iterates with line numbers.
- UTF-8 — recommended encoding for text files.

# 2. pathlib — Paths and Directories

- `Path()` — creates a path object (cross-platform).
- `Path.cwd()` — current working directory.
- `Path.home()` — user's home directory.
- `path / "file.txt"` — joins paths.
- `path.parent` — parent directory.
- `path.name` — filename with extension.
- `path.stem` — filename without extension.
- `path.suffix` — file extension.

**Files and directories:**
```python
from pathlib import Path

folder = Path("data/logs")
folder.mkdir(parents=True, exist_ok=True)

file = folder / "access.log"
file.write_text("Hello\n", encoding="utf-8")
content = file.read_text(encoding="utf-8")
```

- `exists()` — checks if a path exists.
- `is_file()` / `is_dir()` — checks path type.
- `mkdir(parents=True, exist_ok=True)` — creates directories.
- `stat().st_size` — file size in bytes.
- `write_text()` — creates/overwrites a file.
- `read_text()` — reads the entire file into memory.

**Finding files:**
```python
folder.glob("*.log")   # Current directory
folder.rglob("*.log")  # Including subdirectories
```

**Important:** Avoid `read_text()` for large files. Use `with open(...)` and iterate line by line instead.

# 3. os & shutil — File Operations

- `os` — operating system operations and environment variables.
- `shutil` — high-level file and directory operations.

**Copying and moving:**
```python
import shutil

shutil.copy(source, destination)   # Copy file
shutil.copy2(source, destination)  # Copy with metadata
shutil.move(source, destination)   # Move file or directory
```

**Renaming and deleting:**
```python
from pathlib import Path

file = Path("data/access.log")

file.rename("data/server.log")  # Rename or move
file.unlink()                   # Delete file
file.unlink(missing_ok=True)    # Ignore missing file
```

**Directories:**
- `Path.rmdir()` / `os.rmdir()` — remove empty directory.
- `shutil.rmtree(path)` — remove directory and all contents.

**Useful os functions:**
```python
import os

os.getcwd()         # Current working directory
os.listdir("data")  # List directory contents
os.getenv("HOME")   # Read environment variable
```

**Important:**
- `copy()` preserves the original; `move()` relocates it.
- `copy2()` also attempts to preserve metadata (e.g. modification time).
- Copying to an existing file can overwrite it.
- `shutil.rmtree()` permanently removes the entire directory tree — use with caution.
- Prefer `pathlib` for path manipulation and `shutil` for copying/moving files.

# 4. JSON — Serialization and File Handling

- JSON (JavaScript Object Notation) — text-based data format.
- **Serialization** — converting Python objects to JSON.
- **Deserialization** — converting JSON to Python objects.

**Main functions:**
- `json.dump(data, file)` — Python → JSON file.
- `json.load(file)`       — JSON file → Python.
- `json.dumps(data)`      — Python → JSON string.
- `json.loads(string)`    — JSON string → Python.

**Reading and writing:**
```python
import json

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

**JSON types:**
- `dict` → object, `list` → array.
- `True` / `False` → `true` / `false`.
- `None` → `null`.
- Object keys must be strings.

**Custom serialization:**
```python
from datetime import datetime

data = {"timestamp": datetime.now().isoformat()}
```
- Unsupported types (e.g. `datetime`, `Path`) require conversion or a custom serializer (`default=`).

**Error handling:**
```python
try:
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("File not found")
except json.JSONDecodeError:
    print("Invalid JSON")
```

**Important:**
- `indent=4` — pretty formatting.
- `ensure_ascii=False` — preserves non-ASCII characters.
- `json.load()` loads the entire JSON document into memory, so avoid it for very large files.

# 5. CSV — Reading and Writing

- CSV (Comma-Separated Values) — text format for tabular data.
- `csv` — built-in Python module.
- CSV values are read as strings, requiring conversion (e.g. `int()`).

**Reading CSV:**
```python
import csv

with open("data.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"])
```

- `csv.reader()` — returns rows as lists.
- `csv.DictReader()` — returns rows as dictionaries using column headers.

**Writing CSV:**
```python
with open("data.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Adam", "age": 25})
```

- `csv.writer()` / `csv.DictWriter()` — write lists / dictionaries.
- `writerow()` — writes one row.
- `writerows()` — writes multiple rows.
- `writeheader()` — writes column names.
- `delimiter=";"` — specifies a custom separator.
- `newline=""` — ensures correct newline handling.

**Excel — openpyxl:**
```python
from openpyxl import Workbook, load_workbook

wb = Workbook()
ws = wb.active
ws.append(["Name", "Age"])
wb.save("data.xlsx")

wb = load_workbook("data.xlsx", read_only=True)
wb.close()
```

**Important:**
- CSV is suitable for flat, tabular data; JSON supports nested structures.
- Iterate over CSV rows to process large files efficiently.
- Avoid `list(reader)` for large datasets — it loads all rows into memory.
- `openpyxl` handles `.xlsx` files, while `csv` handles plain-text CSV files.

# 6. TOML & YAML — Configuration Files

- **TOML** — configuration format commonly used in Python (`pyproject.toml`).
- **YAML** — configuration format used in DevOps (GitHub Actions, Docker, Kubernetes).
- Both support nested structures, comments (`#`), and human-readable configuration.

**TOML — Reading & Writing:**
```python
import tomllib
import tomli_w

# Read TOML (built-in Python 3.11+)
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# Write TOML (external library)
with open("config.toml", "wb") as f:
    tomli_w.dump(config, f)
```

- `tomllib` — read-only, requires binary mode (`rb`).
- `tomli_w` — writes TOML (`wb`).

**YAML — Reading & Writing:**
```python
import yaml

with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)

with open("config.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(config, f, sort_keys=False)
```

- `yaml.safe_load()` — safely parses standard YAML data.
- `yaml.safe_dump()` — serializes Python data to YAML.
- YAML uses indentation (spaces, not tabs).

**Error Handling:**
- `tomllib.TOMLDecodeError` — invalid TOML.
- `yaml.YAMLError` — invalid YAML.
- `FileNotFoundError` — missing configuration file.

**Important:**
- JSON — data exchange; TOML — Python configuration; YAML — DevOps configuration.
- Never use `yaml.unsafe_load()` with untrusted data.
- Libraries: `uv add tomli-w pyyaml`.

# 7. Binary Files & Pickle

- **Text files** — decoded into `str` using encoding (e.g. UTF-8).
- **Binary files** — raw bytes (`bytes`), without encoding.
- `rb` / `wb` — read/write files in binary mode.

**Encoding & Decoding:**
```python
text = "Hello"
binary = text.encode("utf-8")    # str → bytes
decoded = binary.decode("utf-8") # bytes → str
```

**Binary File Operations:**
```python
with open("data.bin", "wb") as f:
    f.write(b"Hello")

with open("data.bin", "rb") as f:
    data = f.read()
```

**Reading Large Files in Chunks:**
```python
with open("large.bin", "rb") as f:
    while chunk := f.read(1024 * 1024):
        process(chunk)
```
- Reads up to 1 MiB at a time instead of loading the entire file into memory.
- `:=` (walrus operator) — assigns a value within an expression.

**Pickle — Object Serialization:**
```python
import pickle

with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

with open("data.pkl", "rb") as f:
    data = pickle.load(f)
```

- `dump()` / `load()` — serialize/deserialize using files.
- `dumps()` / `loads()` — serialize/deserialize using bytes.
- Supports many Python-specific objects, unlike JSON.

**Important:**
- `bytes` contains integers from 0 to 255.
- UTF-8 characters may occupy multiple bytes.
- **Never unpickle untrusted data** — `pickle.load()` can execute arbitrary code.
- Prefer JSON for safe, portable data exchange.

# 8. Temporary Files & Atomic Writes

- `tempfile` — built-in module for temporary files and directories.
- **Atomic write** — writes to a temporary file first, then replaces the original to prevent partial updates.

**Temporary Files:**
```python
import tempfile

with tempfile.TemporaryFile(mode="w+t") as f:
    f.write("Hello")
    f.seek(0)  # Move cursor to beginning
    print(f.read())
```

- `TemporaryFile()` — automatically deleted after closing.
- `NamedTemporaryFile()` — temporary file with an accessible path (`f.name`).
- `TemporaryDirectory()` — temporary directory, automatically removed.
- `seek(0)` — moves the file cursor to the beginning.

**Atomic Write:**
```python
import os
import json
import tempfile
from pathlib import Path

destination = Path("stats.json")
temp_path = None

try:
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=destination.parent,
        delete=False,
    ) as f:
        temp_path = Path(f.name)
        json.dump({"requests": 1500}, f, indent=4)

    os.replace(temp_path, destination)
finally:
    if temp_path is not None:
        temp_path.unlink(missing_ok=True)
```

**Important:**
- `os.replace()` — atomically replaces the destination on supported filesystems.
- Keep temporary and destination files on the same filesystem.
- `delete=False` — prevents automatic deletion before replacement.
- Use `try/finally` to clean up temporary files after errors.
- Atomicity prevents partial replacement, but does not guarantee durability after power loss (`fsync()` may be needed).
- `pytest` provides the `tmp_path` fixture for testing file operations.

# 9. Command-Line Arguments — sys.argv & argparse

- `sys.argv` — list of CLI arguments (`argv[0]` is the script name).
- `argparse` — built-in module for parsing and validating CLI arguments.

**Argument Parsing:**
```python
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Server Log Parser")

parser.add_argument("file", type=Path)  # Required positional
parser.add_argument("--output", default="stats.json")
parser.add_argument("--format", choices=["csv", "json"], default="json")
parser.add_argument("--top", type=int, default=10)
parser.add_argument("--verbose", action="store_true")

args = parser.parse_args()
```

**Common Options:**
- `type` — converts input to a specific type.
- `default` — default value if omitted.
- `required=True` — makes an optional argument mandatory.
- `choices` — restricts allowed values.
- `action="store_true"` — boolean flag (`False` by default).
- `--help` — automatically displays CLI documentation.

**Validation & Error Handling:**
```python
if not args.file.is_file():
    parser.error("Input file not found")

if args.top <= 0:
    parser.error("--top must be positive")
```

- `parser.error()` — displays a readable error without a traceback and exits with code `2`.
- Prefer `argparse` over `sys.argv` for complex CLIs.