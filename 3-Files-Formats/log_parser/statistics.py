from collections import Counter
from datetime import datetime
from typing import Literal

from .parser import LogEntry


def count_by_field(
    logs: list[LogEntry], field: Literal["status", "ip"]
) -> Counter[int | str]:
    counter: Counter[int | str] = Counter()

    for log in logs:
        counter[log[field]] += 1

    return counter


def traffic_per_hour(logs: list[LogEntry]) -> dict[str, dict[str, int]]:
    traffic: dict[str, dict[str, int]] = {}

    for log in logs:
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

    return traffic


if __name__ == "__main__":
    from pathlib import Path

    from .parser import parse_log_line

    file_path = Path("data/access.log")

    with open(file_path, "r", encoding="utf-8") as f:
        logs = [parse_log_line(line) for line in f]

    print(count_by_field(logs, "status"))
    print(count_by_field(logs, "ip"))

    traffic = traffic_per_hour(logs)

    for hour, stats in sorted(traffic.items()):
        print(f"{hour}: {stats['requests']} requests, {stats['bytes']} bytes")
