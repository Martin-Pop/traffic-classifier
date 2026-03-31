import logging
import os
import sys

from common.logger import configure_file_loggers, configure_console_loggers
from common.file import try_load_json_from_file, get_absolute_path, calculate_file_hash
from configuration.configurations import AppConfiguration

log = logging.getLogger(__name__)

if __name__ == "__main__":

    config_file = get_absolute_path(os.path.join("configuration", "config.json"))
    err_log_file = get_absolute_path(os.path.join("logs", "error.log"))
    app_log_file = get_absolute_path(os.path.join("logs", "app.log"))

    json, err = try_load_json_from_file(config_file)
    configure_file_loggers(err_log_file, app_log_file)
    configure_console_loggers()

    if err:
        log.error("Failed to parse configuration: "+ err)
        sys.exit(1)

    configuration = AppConfiguration(**json)
    print(configuration.__dict__)

    print(calculate_file_hash(get_absolute_path("test.pcap")))
