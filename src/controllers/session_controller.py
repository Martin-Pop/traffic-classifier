import logging
import os

from PySide6.QtCore import Signal, QObject

from common.file import get_formatted_file_size
from core.reports import AnalysedReports
from view.window.report_configuration import ReportConfigurationWindow

log = logging.getLogger("SessionController")


class SessionController(QObject):

    session_closed = Signal(object)

    def __init__(self, configuration):
        super().__init__()
        self._configuration = configuration
        self._analysed_reports = AnalysedReports(configuration.analysed_captures_directory)
        self._report_config_window = None
        self._info = None


    def start(self, file_path):
        self._info = {
            "name": os.path.basename(file_path),
            "size": get_formatted_file_size(file_path),
            "saved_reports": self._analysed_reports.get_reports_for_file(file_path),
        }

        self._report_config_window = ReportConfigurationWindow(self._info)
        self._report_config_window.closed_signal.connect(self._on_report_closed)
        self._report_config_window.show()

        log.info(f"Report configuration started for {self._info.get('name')}")

    def _on_report_closed(self):
        self.session_closed.emit(self)
        log.info(f"Report configuration ended for {self._info.get('name')}")