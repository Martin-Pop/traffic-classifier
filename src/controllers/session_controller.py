import os

from PySide6.QtCore import Signal, QObject

from common.file import get_formatted_file_size
from core.reports import AnalysedReports
from view.report_configuration import ReportConfigurationWindow


class SessionController(QObject):

    session_closed = Signal(object)

    def __init__(self, configuration):
        super().__init__()
        self._configuration = configuration
        self._analysed_reports = AnalysedReports(configuration.analysed_captures_directory)
        self._report_config_window = None


    def start(self, file_path):
        info = {
            "name": os.path.basename(file_path),
            "size": get_formatted_file_size(file_path),
            "saved_reports": self._analysed_reports.get_reports_for_file(file_path),
        }

        self._report_config_window = ReportConfigurationWindow(info)
        self._report_config_window.show()