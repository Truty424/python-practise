import csv
import json
from pathlib import Path

import pytest

from log_parser.exporter import export_csv, export_json
from log_parser.statistics import LogStatistics


@pytest.fixture
def sample_stats() -> LogStatistics:
    return {
        "total_requests": 3,
        "status_codes": {200: 2, 404: 1},
        "top_ips": [
            ("192.168.1.10", 2),
            ("10.0.0.5", 1),
        ],
        "traffic_per_hour": {
            "2026-11-12 10:00 +0100": {
                "requests": 2,
                "bytes": 300,
            },
            "2026-11-12 11:00 +0100": {
                "requests": 1,
                "bytes": 400,
            },
        },
    }


def test_export_json(
    sample_stats: LogStatistics,
    tmp_path: Path,
) -> None:
    output_file = tmp_path / "output" / "stats.json"

    export_json(sample_stats, output_file)

    assert output_file.exists()

    with open(output_file, encoding="utf-8") as f:
        result = json.load(f)

    assert result["total_requests"] == 3
    assert result["status_codes"] == {
        "200": 2,
        "404": 1,
    }
    assert result["top_ips"] == [
        ["192.168.1.10", 2],
        ["10.0.0.5", 1],
    ]
    assert result["traffic_per_hour"] == sample_stats["traffic_per_hour"]


def read_csv(file_path: Path) -> list[list[str]]:
    with open(file_path, encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def test_export_csv(
    sample_stats: LogStatistics,
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "output"

    export_csv(sample_stats, output_dir)

    for filename in ["status_codes.csv", "top_ips.csv", "traffic_per_hour.csv"]:
        assert (output_dir / filename).exists()

    assert read_csv(output_dir / "status_codes.csv") == [
        ["status_code", "count"],
        ["200", "2"],
        ["404", "1"],
    ]

    assert read_csv(output_dir / "top_ips.csv") == [
        ["ip", "requests"],
        ["192.168.1.10", "2"],
        ["10.0.0.5", "1"],
    ]

    assert read_csv(output_dir / "traffic_per_hour.csv") == [
        ["hour", "requests", "bytes"],
        ["2026-11-12 10:00 +0100", "2", "300"],
        ["2026-11-12 11:00 +0100", "1", "400"],
    ]
