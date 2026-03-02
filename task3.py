import sys
from collections import defaultdict


def parse_log_line(line: str) -> dict:
    parts = line.split(None, 3)
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "message": parts[3].strip() if len(parts) > 3 else "",
    }


def load_logs(file_path: str) -> list:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [parse_log_line(line) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        sys.exit(1)
    except OSError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda log: log["level"].upper() == level.upper(), logs))


def count_logs_by_level(logs: list) -> dict:
    counts = defaultdict(int)
    for log in logs:
        counts[log["level"]] += 1
    return dict(counts)


def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<17}| Кількість")
    print(f"{'-' * 17}|{'-' * 10}")
    for level, count in counts.items():
        print(f"{level:<17}| {count}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task3.py <log_file> [level]")
        sys.exit(1)

    log_file = sys.argv[1]
    logs = load_logs(log_file)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) >= 3:
        level = sys.argv[2].upper()
        filtered = filter_logs_by_level(logs, level)
        print(f"\nДеталі логів для рівня '{level}':")
        for log in filtered:
            print(f"{log['date']} {log['time']} - {log['message']}")
