import logging
import os
import sys

from PySide6.QtWidgets import QApplication

from common.logger import configure_file_loggers, configure_console_loggers
from common.file import try_load_json_from_file, get_absolute_path
from configuration.configurations import AppConfiguration
from view.style_loader import apply_stylesheet
from view.window.main_window import MainWindow

log = logging.getLogger(__name__)

if __name__ == "__main__":

    # TODO: fix logs folder not existing
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
    configuration.model_path = get_absolute_path(configuration.model_path) # converts relative to abs path

    app = QApplication(sys.argv)
    apply_stylesheet(app)

    window = MainWindow(configuration)
    window.show()

    sys.exit(app.exec())
