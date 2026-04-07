import csv
from datetime import datetime
from pathlib import Path

from common.file import calculate_file_hash, get_absolute_path
from common.utils import is_valid_ip

def _to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

class AnalysedCaptures:

    def __init__(self, captures_directory):
        self._directory = get_absolute_path(captures_directory)
        self._found_captures = None
        self._hash = None

    def get_saved_captures(self, ip_address):
        if ip_address not in self._found_captures.keys():
            return None

        file_path = self._found_captures[ip_address][0]

        if not Path(file_path).exists():
            return None

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = list(reader)

        return [ {k: _to_float(v) for k, v in row.items()} for row in data ]

    def find_captures_for_file(self, file_path):
        self._hash = calculate_file_hash(file_path)
        self._found_captures = self._find_analysed_captures(self._hash)

        return self._found_captures

    def save_captures(self, analysed_captures, ip_address):
        formatted_ip = ip_address.replace('.', '_')
        file_name = formatted_ip + "_" + self._hash + ".csv"
        file_path = Path(self._directory).joinpath(file_name)

        if not analysed_captures:
            return

        fieldnames = analysed_captures[0].keys()

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(analysed_captures)

    def _find_analysed_captures(self, target_hash):
        reports = {}

        for item in Path(self._directory).iterdir():
            if not item.is_file():
                continue

            if item.suffix != ".csv":
                continue

            parts = item.stem.split("_")

            if len(parts) < 5:
                continue

            ip_parts = parts[:4]
            file_hash = parts[4]

            if file_hash != target_hash:
                continue

            ip = ".".join(ip_parts)
            if not is_valid_ip(ip):
                continue

            stat = item.stat()
            modified_time = datetime.fromtimestamp(stat.st_mtime)

            reports[ip] = (str(item.resolve()), modified_time)

        return reports