from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCharts import QChart,  QSplineSeries, QDateTimeAxis, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen

import sys
from common.file import get_absolute_path

vendor_path = get_absolute_path(".")
sys.path.append(vendor_path)

from vendor.interactive_chart import InteractiveChartView


class TrafficChartPage(QWidget):
    def __init__(self, results_list):
        super().__init__()

        self._category_config = {
            'browsing': {'color': '#33cc33', 'series': QSplineSeries()},
            'download': {'color': '#0099ff', 'series': QSplineSeries()},
            'gaming': {'color': '#ff0000', 'series': QSplineSeries()},
            'idle': {'color': '#cccccc', 'series': QSplineSeries()},
            'video': {'color': '#ff9900', 'series': QSplineSeries()},
            'voice': {'color': '#9900cc', 'series': QSplineSeries()}
        }

        self._results_data = sorted(results_list, key=lambda x: x['timestamp'])
        self._process_data()
        self._init_ui()

    def _process_data(self):
        for entry in self._results_data:
            ts = entry['timestamp']
            for category, config in self._category_config.items():
                value = entry.get(category, 0.0)
                config['series'].append(ts * 1000, value)

    def _init_ui(self):
        self.setObjectName("background")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.chart = QChart()
        self.chart.setBackgroundVisible(True)
        self.chart.setBackgroundBrush(QBrush(QColor("white")))

        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        for category, config in self._category_config.items():
            series = config['series']
            series.setName(category.capitalize())

            pen = QPen(QColor(config['color']))
            pen.setWidth(3)
            series.setPen(pen)

            self.chart.addSeries(series)

        axis_x = QDateTimeAxis()
        axis_x.setFormat("HH:mm:ss")
        axis_x.setTitleText("Time")
        axis_x.setTickCount(8)
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

        axis_y = QValueAxis()
        axis_y.setRange(0.0, 100.0)
        axis_y.setTitleText("Probability (%)")
        axis_y.setLabelFormat("%.1f")
        axis_y.setTickCount(6)
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        for category, config in self._category_config.items():
            config['series'].attachAxis(axis_x)
            config['series'].attachAxis(axis_y)

        self.chart_view = InteractiveChartView(self.chart, self._results_data, self._category_config)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setObjectName("chart_view")

        main_layout.addWidget(self.chart_view)