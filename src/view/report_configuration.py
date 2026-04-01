from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QFrame
)

class ReportConfigurationWindow(QWidget):
    def __init__(self, file_info):
        super().__init__()
        self._file_info = file_info

        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Report Configuration")
        self.resize(450, 350)

        self.setObjectName("main_window")
        self.setStyleSheet("""
            #main_window {
                background-color: #f9f9f9;
            }
            #lbl_filename {
                font-size: 18px; 
                font-weight: bold; 
                color: #3c3c3c;
            }
            #lbl_size {
                color: #3c3c3c; 
                font-size: 13px;
            }
            #cache_frame {
                background-color: #e6e6e6;
                border: 1px solid #ccc; 
                border-radius: 8px;
            }
            #lbl_status {
                color: #3c3c3c; 
                font-weight: bold; 
                border: none;
            }
            #lbl_item {
                border: none; 
                color: #555; 
                margin-left: 10px;
            }
            #chk_reanalyze {
                font-weight: bold; 
                margin-top: 10px;
                color: #3c3c3c;
            }
            #lbl_ip_input {
                font-weight: bold;
                color: #3c3c3c;
            }
            #input_ip {
                padding: 8px;
                border: 1px solid #aaa;
                border-radius: 4px;
                background-color: #fff;
                color: #3c3c3c;
            }
            #btn {
                padding: 8px; 
                background-color: #3359cc; 
                border-radius: 4px;
                font-size: 12px;
                color: #e8e8e8;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # file name
        self.lbl_filename = QLabel(f"File: {self._file_info.get('name')}")
        self.lbl_filename.setObjectName("lbl_filename")
        main_layout.addWidget(self.lbl_filename)

        # file size
        self.lbl_size = QLabel(f"Size: {self._file_info.get('size')}")
        self.lbl_size.setObjectName("lbl_size")
        main_layout.addWidget(self.lbl_size)

        # saved reports
        saved_reports = self._file_info.get('saved_reports')
        if saved_reports:

            cache_frame = QFrame()
            cache_frame.setObjectName("cache_frame")
            cache_layout = QVBoxLayout(cache_frame)

            lbl_status = QLabel("Already processed for:")
            lbl_status.setObjectName("lbl_status")
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
        lbl_ip_input.setObjectName("lbl_ip_input")

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
        self.btn_exit.setObjectName("btn")
        self.btn_exit.setMinimumWidth(100)

        self.btn_report = QPushButton("Generate Report")
        self.btn_report.setObjectName("btn")
        self.btn_report.setMinimumWidth(100)

        btn_layout.addWidget(self.btn_exit)
        btn_layout.addWidget(self.btn_report)

        main_layout.addLayout(btn_layout)