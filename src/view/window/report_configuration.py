from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QFrame, QMessageBox
)

from common.utils import is_valid_ip


def _show_invalid_ip_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle("Invalid IP")
    msg.setText("IP address is not valid!")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()

class LabelWithValue(QWidget):
    def __init__(self, label, value):
        super().__init__()
        self._label = label
        self._value = value
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        lbl_title = QLabel(self._label)
        lbl_value = QLabel(self._value)
        lbl_value.setObjectName("value_label")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        layout.addStretch()

class ReportConfigurationWindow(QWidget):
    closed_signal = Signal()
    submit_signal = Signal(str)

    def __init__(self, file_info):
        super().__init__()
        self._file_info = file_info
        self._init_ui()

    def closeEvent(self, event):
        self.closed_signal.emit()
        event.accept()

    def _init_ui(self):
        self.setWindowTitle(f"Report Configuration - {self._file_info.get('name')}")
        self.resize(450, 350)
        self.setObjectName("background")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # file name
        file_name_lbl = LabelWithValue("File Name:", self._file_info.get("name"))
        main_layout.addWidget(file_name_lbl)

        # file size
        lbl_size = LabelWithValue(f"Size:", self._file_info.get('size'))
        main_layout.addWidget(lbl_size)

        # saved captures
        saved_captures = self._file_info.get('saved_captures')
        if saved_captures:

            cache_frame = QFrame()
            cache_frame.setObjectName("background_frame")
            cache_layout = QVBoxLayout(cache_frame)

            lbl_status = QLabel("Saved analysed captures:")
            cache_layout.addWidget(lbl_status)

            for k, v in saved_captures.items():
                lbl_item = QLabel(f"• IP: {k} - {v[1].strftime('%Y-%m-%d %H:%M:%S')}")
                lbl_item.setObjectName("value_label")
                cache_layout.addWidget(lbl_item)

            main_layout.addWidget(cache_frame)

            self.checkbox = QCheckBox("Force new analysis")
            self.checkbox.setObjectName("chk_reanalyze")
            main_layout.addWidget(self.checkbox)

        # target ip
        ip_layout = QVBoxLayout()
        ip_layout.setSpacing(5)

        lbl_ip_input = QLabel("Target IP address:")

        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText("192.168.1.50")

        ip_layout.addWidget(lbl_ip_input)
        ip_layout.addWidget(self.input_ip)
        main_layout.addLayout(ip_layout)

        main_layout.addStretch()

        # buttons
        btn_layout = QHBoxLayout()

        self.btn_exit = QPushButton("Cancel")
        self.btn_exit.setMinimumWidth(100)
        self.btn_exit.clicked.connect(self.close)

        self.btn_report = QPushButton("Generate Report")
        self.btn_report.setMinimumWidth(100)
        self.btn_report.clicked.connect(self._on_generate_report)

        btn_layout.addWidget(self.btn_exit)
        btn_layout.addWidget(self.btn_report)

        main_layout.addLayout(btn_layout)

    def _on_generate_report(self):
        target_ip = self.input_ip.text()
        if not is_valid_ip(target_ip):
            _show_invalid_ip_message()
        else:
            #just ip for now
            self.submit_signal.emit(self.input_ip.text())