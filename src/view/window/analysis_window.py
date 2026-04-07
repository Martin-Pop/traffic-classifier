import logging

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton

log = logging.getLogger("AnalysisWindow")

class AnalysisWindow(QWidget):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._pages = {}
        self._init_ui()

    def switch_page_to(self, page_name):
        target_widget = self._pages.get(page_name)
        if target_widget:
            self.page_container.setCurrentWidget(target_widget)
        else:
            log.error(f"Page '{page_name}' was not found")

    def add_page(self, page_name, page_widget, accessible=True):
        self.page_container.addWidget(page_widget)

        if accessible:
            self._pages[page_name] = page_widget

            button = QPushButton(page_name)
            button.clicked.connect(lambda: self.switch_page_to(page_name))
            self.button_layout.addWidget(button)


    def _init_ui(self):
        self.setObjectName("background")
        self.setWindowTitle(f"Analysis results - {self._file_name}")
        self.resize(720, 480)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5,5,5,5)

        button_container = QWidget(self)
        self.button_layout = QHBoxLayout(button_container)
        self.button_layout.setContentsMargins(0,0,0,0)

        self.page_container = QStackedWidget(self)

        main_layout.addWidget(button_container)
        main_layout.addWidget(self.page_container)