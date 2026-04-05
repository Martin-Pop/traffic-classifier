from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class AnalysisProgressPage(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def update_label(self, text):
        self._label.setText(text)

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self._label = QLabel("Analysis results")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self._label)