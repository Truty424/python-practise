import csv
import json
import tomllib
from pathlib import Path

import pytest

from log_parser.converter import (
    csv_to_json,
    csv_to_toml,
    json_to_csv,
    json_to_toml,
    toml_to_csv,
    toml_to_json,
)


def test_csv_to_json(tmp_path: Path) -> None:
    input_file = tmp_path / "users.csv"
    output_file = tmp_path / "users.json"

    input_file.write_text(
        "name,age,city\nAdam,25,Gdańsk\nAnna,30,Warszawa\n",
        encoding="utf-8",
    )

    csv_to_json(input_file, output_file)

    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data == [
        {"name": "Adam", "age": "25", "city": "Gdańsk"},
        {"name": "Anna", "age": "30", "city": "Warszawa"},
    ]


def test_json_to_csv(tmp_path: Path) -> None:
    input_file = tmp_path / "users.json"
    output_file = tmp_path / "users.csv"

    users = [
        {"name": "Adam", "age": "25", "city": "Gdańsk"},
        {"name": "Anna", "age": "30", "city": "Warszawa"},
    ]

    input_file.write_text(
        json.dumps(users, ensure_ascii=False),
        encoding="utf-8",
    )

    json_to_csv(input_file, output_file)

    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["name", "age", "city"]
        result = list(reader)

    assert result == users


def test_json_to_csv_empty_list(tmp_path: Path) -> None:
    input_file = tmp_path / "empty.json"
    output_file = tmp_path / "output.csv"

    input_file.write_text("[]", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="JSON must contain a non-empty list of records",
    ):
        json_to_csv(input_file, output_file)

    assert not output_file.exists()


def test_json_to_csv_invalid_record(tmp_path: Path) -> None:
    input_file = tmp_path / "invalid.json"
    output_file = tmp_path / "output.csv"

    record = [
        {"name": "Adam"},
        123,
    ]

    input_file.write_text(
        json.dumps(record),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="All records must be dictionaries",
    ):
        json_to_csv(input_file, output_file)

    assert not output_file.exists()


def test_json_to_csv_inconsistent_fields(tmp_path: Path) -> None:
    input_file = tmp_path / "invalid.json"
    output_file = tmp_path / "output.csv"

    record = [
        {"name": "Adam", "age": "25"},
        {"name": "Anna", "city": "Gdańsk"},
    ]

    input_file.write_text(
        json.dumps(record),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="All records must have the same fields",
    ):
        json_to_csv(input_file, output_file)

    assert not output_file.exists()


def test_json_to_toml(tmp_path: Path) -> None:
    input_file = tmp_path / "users.json"
    output_file = tmp_path / "output" / "users.toml"

    users = [
        {"name": "Adam", "age": 25, "city": "Gdańsk"},
        {"name": "Anna", "age": 30, "city": "Warszawa"},
    ]

    input_file.write_text(
        json.dumps(users, ensure_ascii=False),
        encoding="utf-8",
    )

    json_to_toml(input_file, output_file)

    assert output_file.exists()

    with open(output_file, "rb") as f:
        data = tomllib.load(f)

    assert data == {"records": users}


def test_toml_to_json(tmp_path: Path) -> None:
    input_file = tmp_path / "users.toml"
    output_file = tmp_path / "output" / "users.json"

    input_file.write_text(
        "[[records]]\n"
        'name = "Adam"\n'
        "age = 25\n"
        'city = "Gdańsk"\n'
        "\n"
        "[[records]]\n"
        'name = "Anna"\n'
        "age = 30\n"
        'city = "Warszawa"\n',
        encoding="utf-8",
    )

    toml_to_json(input_file, output_file)

    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as f:
        result = json.load(f)

    assert result == [
        {"name": "Adam", "age": 25, "city": "Gdańsk"},
        {"name": "Anna", "age": 30, "city": "Warszawa"},
    ]


def test_json_toml_round_trip(tmp_path: Path) -> None:
    original_file = tmp_path / "original.json"
    toml_file = tmp_path / "converted.toml"
    result_file = tmp_path / "result.json"

    users = [
        {"name": "Adam", "age": 25, "active": True},
        {"name": "Anna", "age": 30, "active": False},
    ]

    original_file.write_text(
        json.dumps(users, ensure_ascii=False),
        encoding="utf-8",
    )

    json_to_toml(original_file, toml_file)
    toml_to_json(toml_file, result_file)

    with open(result_file, "r", encoding="utf-8") as f:
        result = json.load(f)

    assert result == users


def test_toml_to_json_missing_records(tmp_path: Path) -> None:
    input_file = tmp_path / "invalid.toml"
    output_file = tmp_path / "output.json"

    input_file.write_text(
        'name = "Adam"\nage = 25\n',
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="TOML must contain a non-empty list of records",
    ):
        toml_to_json(input_file, output_file)

    assert not output_file.exists()


def test_csv_to_toml(tmp_path: Path) -> None:
    input_file = tmp_path / "users.csv"
    output_file = tmp_path / "output" / "users.toml"

    input_file.write_text(
        "name,age,city\nAdam,25,Gdańsk\nAnna,30,Warszawa\n",
        encoding="utf-8",
    )

    csv_to_toml(input_file, output_file)

    assert output_file.exists()

    with open(output_file, "rb") as f:
        result = tomllib.load(f)

    assert result == {
        "records": [
            {"name": "Adam", "age": "25", "city": "Gdańsk"},
            {"name": "Anna", "age": "30", "city": "Warszawa"},
        ]
    }


def test_toml_to_csv(tmp_path: Path) -> None:
    input_file = tmp_path / "users.toml"
    output_file = tmp_path / "output" / "users.csv"

    input_file.write_text(
        "[[records]]\n"
        'name = "Adam"\n'
        "age = 25\n"
        'city = "Gdańsk"\n'
        "\n"
        "[[records]]\n"
        'name = "Anna"\n'
        "age = 30\n"
        'city = "Warszawa"\n',
        encoding="utf-8",
    )

    toml_to_csv(input_file, output_file)

    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        assert reader.fieldnames == ["name", "age", "city"]

        result = list(reader)

    assert result == [
        {"name": "Adam", "age": "25", "city": "Gdańsk"},
        {"name": "Anna", "age": "30", "city": "Warszawa"},
    ]
