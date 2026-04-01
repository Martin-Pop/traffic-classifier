from PySide6.QtCore import Signal, QObject

from view.report_configuration import ReportConfigurationWindow


class SessionController(QObject):

    session_closed = Signal(object)

    def __init__(self, configuration):
        super().__init__()
        self._configuration = configuration

        info = {
            "name": "test.pcap",
            "size": "40Kb",
            "saved_reports": [("192.168.0.4", "somedate"), ("192.168.0.10", "somedate")]
        }

        self._report_config_window = ReportConfigurationWindow(info)
        self._report_config_window.show()

    def open(self):
        pass