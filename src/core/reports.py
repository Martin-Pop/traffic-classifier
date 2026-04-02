from datetime import datetime
from pathlib import Path

from common.file import calculate_file_hash, get_absolute_path
from common.utils import is_valid_ip


class AnalysedReports:

    def __init__(self, reports_directory):
        self._directory = get_absolute_path(reports_directory)
        self._found_reports = None

    def get_reports_for_file(self, file_path):
        file_hash = calculate_file_hash(file_path)
        self._found_reports = self._find_reports(file_hash)
        return self._found_reports

    def save_report(self):
        pass

    def _find_reports(self, target_hash):
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
