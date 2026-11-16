import csv
import json
from collections.abc import Iterable, Sequence
from pathlib import Path

from .statistics import LogStatistics


def export_json(stats: LogStatistics, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)


def export_csv(stats: LogStatistics, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    write_csv(
        output_dir / "status_codes.csv",
        ["status_code", "count"],
        stats["status_codes"].items(),
    )

    write_csv(
        output_dir / "top_ips.csv",
        ["ip", "requests"],
        stats["top_ips"],
    )

    write_csv(
        output_dir / "traffic_per_hour.csv",
        ["hour", "requests", "bytes"],
        (
            (hour, data["requests"], data["bytes"])
            for hour, data in stats["traffic_per_hour"].items()
        ),
    )


def write_csv(
    file_path: Path,
    headers: list[str],
    rows: Iterable[Sequence[str | int]],
) -> None:
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
