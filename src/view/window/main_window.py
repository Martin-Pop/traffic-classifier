from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QFileDialog
)

from controllers.session_controller import SessionController
from core.predictions import ModelService


class DropZone(QLabel):
    file_dropped_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setText("Drag and drop your PCAP file here")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(5,5,5,5)
        self.setAcceptDrops(True)
        self.setObjectName("drop_zone")

        self.style_default = """
            #drop_zone {
                border: 4px dashed #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
                font-size: 18px;
                color: #555;
            }
            #drop_zone:hover {
                background-color: #e9e9e9;
                border-color: #888;
                color: #333;
            }
        """

        self.style_drag = """
            #drop_zone {
                border: 4px solid #4CAF50;
                border-radius: 10px;
                background-color: #e8f5e9;
                font-size: 18px;
                color: #2e7d32;
            }
        """

        self.setStyleSheet(self.style_default)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.endswith(('.pcap', '.pcapng')):
                event.acceptProposedAction()

                self.setStyleSheet(self.style_drag)
            else:
                event.ignore()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.style_default)

    def dropEvent(self, event):
        self.setStyleSheet(self.style_default)
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_dropped_signal.emit(file_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select PCAP file",
                "",
                "PCAP files (*.pcap *.pcapng);"
            )
            if file_path:
                self.file_dropped_signal.emit(file_path)


class MainWindow(QMainWindow):
    def __init__(self, configuration):
        super().__init__()
        self._configuration = configuration
        self._model_service = ModelService(configuration.model_path)
        self._active_sessions = []
        self._drop_zone = None

        self._init_ui()
        self._connect_events()

    def _init_ui(self):
        self.setWindowTitle("Traffic Classifier")
        self.resize(400, 250)

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #e6e6e6;")

        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)

        self._drop_zone = DropZone()
        layout.addWidget(self._drop_zone)

    def _connect_events(self):
        self._drop_zone.file_dropped_signal.connect(self.handle_new_file_dropped)

    def handle_new_file_dropped(self, file_path):
        session = SessionController(self._configuration, self._model_service)
        session.session_closed.connect(self.remove_session)
        self._active_sessions.append(session)

        session.start(file_path)

    def remove_session(self, session_instance):
        if session_instance in self._active_sessions:
            self._active_sessions.remove(session_instance)