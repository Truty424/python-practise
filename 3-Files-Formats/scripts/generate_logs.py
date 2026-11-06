import random
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def generate_log_line() -> str:
    ips = ["192.168.1.10", "10.0.0.5", "172.16.0.1"]
    methods = ["GET", "POST", "DELETE"]
    paths = ["/", "/login", "/api/users"]
    statuses = [200, 404, 500]

    ip = random.choice(ips)
    method = random.choice(methods)
    path = random.choice(paths)
    status = random.choice(statuses)
    size = random.randint(100, 5000)

    timestamp = datetime.now().astimezone().strftime("%d/%b/%Y:%H:%M:%S %z")

    return f'{ip} - - [{timestamp}] "{method} {path} HTTP/1.1" {status} {size}'


def generate_log_file(output_path: Path, count: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(generate_log_line() + "\n" for _ in range(count))


def generate_large_log_file(output_path: Path, size_mb: int) -> None:
    target_size = size_mb * 1024 * 1024

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        while f.tell() < target_size:
            line = generate_log_line() + "\n"
            binary_line = line.encode("utf-8")
            f.write(binary_line)
