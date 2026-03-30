import logging

FILE_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | P:%(process)d | %(message)s"
CONSOLE_LOG_FORMAT = "%(levelname)s | %(message)s"
root_logger = logging.getLogger()

class ExactLevelFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        print(level)
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

    formatter = logging.Formatter(CONSOLE_LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)

    root_logger.addHandler(console_handler)