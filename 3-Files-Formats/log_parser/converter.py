import csv
import json
import tomllib
from pathlib import Path
from tempfile import TemporaryDirectory

import tomli_w


def csv_to_json(input_path: Path, output_path: Path) -> None:
    with open(input_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def json_to_csv(input_path: Path, output_path: Path) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list) or not data:
        raise ValueError("JSON must contain a non-empty list of records")

    if not all(isinstance(row, dict) for row in data):
        raise ValueError("All records must be dictionaries")

    fieldnames = list(data[0].keys())

    if not all(row.keys() == data[0].keys() for row in data):
        raise ValueError("All records must have the same fields")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def json_to_toml(input_path: Path, output_path: Path) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list) or not data:
        raise ValueError("JSON must contain a non-empty list of records")

    if not all(isinstance(row, dict) for row in data):
        raise ValueError("All records must be dictionaries")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        tomli_w.dump({"records": data}, f)


def toml_to_json(input_path: Path, output_path: Path) -> None:
    with open(input_path, "rb") as f:
        data = tomllib.load(f)

    records = data.get("records")

    if not isinstance(records, list) or not records:
        raise ValueError("TOML must contain a non-empty list of records")

    if not all(isinstance(row, dict) for row in records):
        raise ValueError("All records must be dictionaries")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)


def csv_to_toml(input_path: Path, output_path: Path) -> None:
    with TemporaryDirectory() as temp_dir:
        temp_json = Path(temp_dir) / "temp.json"

        csv_to_json(input_path, temp_json)
        json_to_toml(temp_json, output_path)


def toml_to_csv(input_path: Path, output_path: Path) -> None:
    with TemporaryDirectory() as temp_dir:
        temp_json = Path(temp_dir) / "temp.json"

        toml_to_json(input_path, temp_json)
        json_to_csv(temp_json, output_path)
