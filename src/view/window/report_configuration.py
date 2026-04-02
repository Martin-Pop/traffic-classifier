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


class ReportConfigurationWindow(QWidget):
    closed_signal = Signal()
    submit_signal = Signal()

    def __init__(self, file_info):
        super().__init__()
        self._file_info = file_info
        self._init_ui()

    def closeEvent(self, event):
        self.closed_signal.emit()
        event.accept()

    def _init_ui(self):
        self.setWindowTitle("Report Configuration")
        self.resize(450, 350)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # file name
        self.lbl_filename = QLabel(f"File: {self._file_info.get('name')}")
        main_layout.addWidget(self.lbl_filename)

        # file size
        self.lbl_size = QLabel(f"Size: {self._file_info.get('size')}")
        main_layout.addWidget(self.lbl_size)

        # saved reports
        saved_reports = self._file_info.get('saved_reports')
        if saved_reports:

            cache_frame = QFrame()
            cache_frame.setObjectName("background_frame")
            cache_layout = QVBoxLayout(cache_frame)

            lbl_status = QLabel("Already processed for:")
            cache_layout.addWidget(lbl_status)

            for ip_address, timestamp in saved_reports:
                lbl_item = QLabel(f"• IP: {ip_address}  |  Date: {timestamp}")
                lbl_item.setObjectName("lbl_item")
                cache_layout.addWidget(lbl_item)

            self.checkbox = QCheckBox("Force new analysis")
            self.checkbox.setObjectName("chk_reanalyze")
            cache_layout.addWidget(self.checkbox)

            main_layout.addWidget(cache_frame)

        # target ip
        ip_layout = QVBoxLayout()
        ip_layout.setSpacing(5)

        lbl_ip_input = QLabel("Target IP address:")

        self.input_ip = QLineEdit()
        self.input_ip.setObjectName("input_ip")
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