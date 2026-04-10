from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter


class KPICard(QFrame):
    def __init__(self, title, value):
        super().__init__()
        self.setObjectName("kpi_card")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)

        lbl_title = QLabel(title)
        lbl_title.setObjectName("kpi_title")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_value = QLabel(value)
        lbl_value.setObjectName("kpi_value")
        lbl_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)


class DashboardPage(QWidget):
    def __init__(self, results_list):
        super().__init__()

        self._results_data = sorted(results_list, key=lambda x: x['timestamp'])

        self._category_config = {
            'browsing': '#33cc33',
            'download': '#0099ff',
            'gaming': '#ff0000',
            'idle': '#cccccc',
            'video': '#ff9900',
            'voice': '#9900cc'
        }

        self._averages = {}
        self._total_duration = "00:00"
        self._dominant_activity = "None"
        self._avg_confidence = "0%"

        self._process_data()
        self._init_ui()

    def _process_data(self):
        if not self._results_data:
            return

        total_entries = len(self._results_data)
        sums = {cat: 0.0 for cat in self._category_config.keys()}
        confidence_sum = 0.0

        for entry in self._results_data:
            max_prob = 0.0
            for cat in self._category_config.keys():
                val = entry.get(cat, 0.0)
                sums[cat] += val
                if val > max_prob:
                    max_prob = val
            confidence_sum += max_prob

        print(sums)
        print(confidence_sum)
        for cat in sums.keys():
            self._averages[cat] = sums[cat] / total_entries

        if self._averages:
            self._dominant_activity = max(self._averages, key=self._averages.get).capitalize()

        avg_conf = confidence_sum / total_entries
        self._avg_confidence = f"{avg_conf:.1f}%"

        start_ts = self._results_data[0]['timestamp']
        end_ts = self._results_data[-1]['timestamp']
        duration_sec = int(end_ts - start_ts)
        mins, secs = divmod(duration_sec, 60)
        self._total_duration = f"{mins:02d}:{secs:02d}"

    def _init_ui(self):
        self.setObjectName("background")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        cards_layout.addWidget(KPICard("Total Duration", self._total_duration))
        cards_layout.addWidget(KPICard("Dominant Activity", self._dominant_activity))
        cards_layout.addWidget(KPICard("Avg. Confidence", self._avg_confidence))

        main_layout.addLayout(cards_layout)

        self.chart = QChart()
        self.chart.setBackgroundVisible(False)
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

        series = QPieSeries()
        series.setHoleSize(0.4)

        for cat, avg_val in self._averages.items():
            if avg_val > 1.0:
                slice_item = series.append(cat.capitalize(), avg_val)
                slice_item.setBrush(QColor(self._category_config[cat]))

                slice_item.setLabelVisible(True)
                slice_item.setLabel(f"{cat.capitalize()} ({avg_val:.1f}%)")

        self.chart.addSeries(series)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setObjectName("chart_view")

        main_layout.addWidget(self.chart_view)