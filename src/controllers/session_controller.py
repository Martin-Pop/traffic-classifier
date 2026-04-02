import logging
import os

from PySide6.QtCore import Signal, QObject

from common.file import get_formatted_file_size
from core.analyser import Analyzer
from core.reports import AnalysedReports
from view.window.report_configuration import ReportConfigurationWindow

log = logging.getLogger("SessionController")


class SessionController(QObject):

    session_closed = Signal(object)

    def __init__(self, configuration, model_service):
        super().__init__()
        self._configuration = configuration
        self._model_service = model_service
        self._analysed_reports = AnalysedReports(configuration.analysed_captures_directory)
        self._analyser = None
        self._report_config_window = None

        self._info = None
        self._target_ip = None
        self._file_path = None


    def start(self, file_path):
        self._file_path = file_path
        self._info = {
            "name": os.path.basename(file_path),
            "size": get_formatted_file_size(file_path),
            "saved_reports": self._analysed_reports.get_reports_for_file(file_path),
        }

        self._report_config_window = ReportConfigurationWindow(self._info)
        self._report_config_window.closed_signal.connect(self._on_report_closed)
        self._report_config_window.submit_signal.connect(self._on_report_submit)
        self._report_config_window.show()

        log.info(f"Report configuration started for {self._info.get('name')}")

    def _on_report_closed(self):
        # self.session_closed.emit(self)
        log.info(f"Report configuration ended for {self._info.get('name')}")

    def _on_report_submit(self, report_configuration):
        # just ip for now
        self._target_ip = report_configuration
        self._report_config_window.close()

        self.analyzer = Analyzer(self._file_path, self._target_ip, self._model_service)
        self.analyzer.progress_changed.connect(self._on_progress)
        self.analyzer.analysis_finished.connect(self._on_results)
        self.analyzer.error_occurred.connect(self._on_error)
        self.analyzer.start()

    def _on_progress(self, message):
        log.info(f"Progress: {message}")

    def _on_results(self, results):
        for res in results:
            log.info(f"Result: {res}")

    def _on_error(self, error_message):
        log.error(f"Error: {error_message}")