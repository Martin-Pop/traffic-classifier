import logging
import sys
from pathlib import Path

FILE_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | P:%(process)d | %(message)s"
CONSOLE_LOG_FORMAT = "%(levelname)s | %(message)s"
root_logger = logging.getLogger()

class ExactLevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self._level = level

    def filter(self, record):
        return record.levelno == self._level

def configure_file_loggers(error_path: str = "error.log", info_path: str = "info.log"):

    formatter = logging.Formatter(FILE_LOG_FORMAT)

    error_handler = logging.FileHandler(error_path, encoding="utf-8", mode="a")
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.WARNING)

    info_handler = logging.FileHandler(info_path, encoding="utf-8", mode="a")
    info_handler.setFormatter(formatter)
    info_handler.setLevel(logging.INFO)
    info_handler.addFilter(ExactLevelFilter(logging.INFO))

    root_logger.addHandler(error_handler)
    root_logger.addHandler(info_handler)

def configure_console_loggers(debug: bool = False):
    root_logger.setLevel(logging.DEBUG)
    level = logging.DEBUG if debug else logging.INFO

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(level)
    info_handler.addFilter(lambda record: record.levelno <= level)
    info_handler.setFormatter(logging.Formatter(CONSOLE_LOG_FORMAT))

    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(logging.Formatter(CONSOLE_LOG_FORMAT))

    root_logger.addHandler(info_handler)
    root_logger.addHandler(err_handler)

def ensure_log_directory_exists(log_dir: str):
    Path(log_dir).mkdir(parents=True, exist_ok=True)
