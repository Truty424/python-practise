from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import TypedDict

from .parser import LogEntry, parse_log_line


class HourlyTraffic(TypedDict):
    requests: int
    bytes: int


class LogStatistics(TypedDict):
    total_requests: int
    status_codes: dict[int, int]
    top_ips: list[tuple[str, int]]
    traffic_per_hour: dict[str, HourlyTraffic]


def update_statistics(
    log: LogEntry,
    status_counter: Counter[int],
    ip_counter: Counter[str],
    traffic: dict[str, HourlyTraffic],
) -> None:
    status_counter[log["status"]] += 1
    ip_counter[log["ip"]] += 1

    dt = datetime.strptime(
        log["timestamp"],
        "%d/%b/%Y:%H:%M:%S %z",
    )

    hour = dt.strftime("%Y-%m-%d %H:00 %z")

    if hour not in traffic:
        traffic[hour] = {
            "requests": 0,
            "bytes": 0,
        }

    traffic[hour]["requests"] += 1
    traffic[hour]["bytes"] += log["size"]


def analyze_logs(file_path: Path) -> LogStatistics:
    status_counter: Counter[int] = Counter()
    ip_counter: Counter[str] = Counter()
    traffic: dict[str, HourlyTraffic] = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            log = parse_log_line(line)

            update_statistics(
                log,
                status_counter,
                ip_counter,
                traffic,
            )

    return {
        "total_requests": sum(status_counter.values()),
        "status_codes": dict(status_counter),
        "top_ips": ip_counter.most_common(10),
        "traffic_per_hour": dict(sorted(traffic.items())),
    }
