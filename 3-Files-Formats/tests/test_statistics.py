from pathlib import Path

import pytest

from log_parser.statistics import analyze_logs


@pytest.fixture
def sample_log_file(tmp_path: Path) -> Path:
    log_file = tmp_path / "access.log"

    lines = [
        '192.168.1.10 - - [12/Nov/2026:10:15:32 +0100] "GET / HTTP/1.1" 200 100',
        '10.0.0.5 - - [12/Nov/2026:10:45:12 +0100] "GET /login HTTP/1.1" 404 200',
        '192.168.1.10 - - [12/Nov/2026:11:10:05 +0100] "POST /api HTTP/1.1" 200 300',
    ]

    log_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return log_file


def test_analyze_logs(sample_log_file: Path) -> None:
    result = analyze_logs(sample_log_file)

    assert result["total_requests"] == 3
    assert result["status_codes"] == {
        200: 2,
        404: 1,
    }
    assert result["top_ips"] == [
        ("192.168.1.10", 2),
        ("10.0.0.5", 1),
    ]


def test_hourly_traffic(sample_log_file: Path) -> None:
    result = analyze_logs(sample_log_file)

    assert result["traffic_per_hour"] == {
        "2026-11-12 10:00 +0100": {
            "requests": 2,
            "bytes": 300,
        },
        "2026-11-12 11:00 +0100": {
            "requests": 1,
            "bytes": 300,
        },
    }


def test_invalid_log(tmp_path: Path) -> None:
    log_file = tmp_path / "invalid.log"
    log_file.write_text("invalid log\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid log format"):
        analyze_logs(log_file)


def test_empty_file(tmp_path: Path) -> None:
    log_file = tmp_path / "empty.log"
    log_file.touch()

    result = analyze_logs(log_file)

    assert result == {
        "total_requests": 0,
        "status_codes": {},
        "top_ips": [],
        "traffic_per_hour": {},
    }
