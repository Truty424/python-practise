import re
from typing import TypedDict

LOG_PATTERN = (
    r"^(?P<ip>\S+) - - "
    r"\[(?P<timestamp>[^\]]+)\] "
    r'"(?P<request>[^"]+)" '
    r"(?P<status>\d+) "
    r"(?P<size>\d+)$"
)


class LogEntry(TypedDict):
    ip: str
    timestamp: str
    method: str
    path: str
    protocol: str
    status: int
    size: int


def parse_log_line(line: str) -> LogEntry:
    match = re.fullmatch(LOG_PATTERN, line.strip())

    if match is None:
        raise ValueError("Invalid log format")

    data = match.groupdict()
    parts = data["request"].split()
    if len(parts) != 3:
        raise ValueError("Invalid HTTP request format")

    method, path, protocol = parts

    return {
        "ip": data["ip"],
        "timestamp": data["timestamp"],
        "method": method,
        "path": path,
        "protocol": protocol,
        "status": int(data["status"]),
        "size": int(data["size"]),
    }
