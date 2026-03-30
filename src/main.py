import logging
import os
import sys

from common.logger import configure_file_loggers, configure_console_loggers
from common.file import try_load_json_from_file, get_absolute_path

log = logging.getLogger(__name__)

if __name__ == "__main__":

    config_file = get_absolute_path(os.path.join("configuration", "confi.json"))
    err_log_file = get_absolute_path(os.path.join("logs", "error.log"))
    app_log_file = get_absolute_path(os.path.join("logs", "app.log"))

    json, err = try_load_json_from_file(config_file)
    configure_file_loggers(err_log_file, app_log_file)
    configure_console_loggers()

    if err:
        log.error("Failed to load configuration: "+ err)
        sys.exit(1)

