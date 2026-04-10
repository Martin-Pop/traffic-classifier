from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from datetime import datetime


class RawDataPage(QWidget):
    def __init__(self, results_list):
        super().__init__()

        self._results_data = sorted(results_list, key=lambda x: x['timestamp'])
        self._categories = ['browsing', 'download', 'gaming', 'idle', 'video', 'voice']

        self._init_ui()
        self._populate_table()

    def _init_ui(self):
        self.setObjectName("background")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.table = QTableWidget()
        self.table.setObjectName("raw_data_table")

        headers = ["Time"] + [cat.capitalize() for cat in self._categories]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for i in range(1, len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        main_layout.addWidget(self.table)

    def _populate_table(self):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self._results_data))

        for row, entry in enumerate(self._results_data):
            dt = datetime.fromtimestamp(entry['timestamp'])
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")

            time_item = QTableWidgetItem(time_str)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, time_item)

            for col, cat in enumerate(self._categories, start=1):
                val = entry.get(cat, 0.0)

                item = QTableWidgetItem(f"{val:.2f}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

        self.table.setSortingEnabled(True)