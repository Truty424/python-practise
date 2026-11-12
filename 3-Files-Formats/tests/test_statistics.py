import pytest

from log_parser.parser import LogEntry, parse_log_line
from log_parser.statistics import count_by_field, traffic_per_hour


@pytest.fixture
def sample_logs() -> list[LogEntry]:
    lines = [
        '192.168.1.10 - - [12/Nov/2026:10:15:32 +0100] "GET / HTTP/1.1" 200 100',
        '10.0.0.5 - - [12/Nov/2026:10:45:12 +0100] "GET /login HTTP/1.1" 404 200',
        '192.168.1.10 - - [12/Nov/2026:11:10:05 +0100] "POST /api HTTP/1.1" 200 300',
    ]

    return [parse_log_line(line) for line in lines]


def test_count_status_codes(sample_logs: list[LogEntry]) -> None:
    result = count_by_field(sample_logs, "status")

    assert result == {200: 2, 404: 1}


def test_count_ips(sample_logs: list[LogEntry]) -> None:
    result = count_by_field(sample_logs, "ip")

    assert result == {
        "192.168.1.10": 2,
        "10.0.0.5": 1,
    }


def test_traffic_per_hour(sample_logs: list[LogEntry]) -> None:
    result = traffic_per_hour(sample_logs)

    assert result == {
        "2026-11-12 10:00 +0100": {
            "requests": 2,
            "bytes": 300,
        },
        "2026-11-12 11:00 +0100": {
            "requests": 1,
            "bytes": 300,
        },
    }


def test_empty_logs() -> None:
    assert count_by_field([], "status") == {}
    assert count_by_field([], "ip") == {}
    assert traffic_per_hour([]) == {}
