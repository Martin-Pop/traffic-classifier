from datetime import datetime

from PySide6.QtCharts import QChartView
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QGraphicsLineItem, QToolTip

# THIS CLASS IS AI GENERATED

class InteractiveChartView(QChartView):
    def __init__(self, chart, results_data, category_config):
        super().__init__(chart)
        self.results_data = results_data
        self.category_config = category_config

        self.setMouseTracking(True)

        self.crosshair = QGraphicsLineItem()
        crosshair_pen = QPen(QColor("#888888"), 1, Qt.PenStyle.DashLine)
        self.crosshair.setPen(crosshair_pen)
        self.crosshair.setZValue(10)
        self.chart().scene().addItem(self.crosshair)
        self.crosshair.hide()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        pos = event.position()

        if self.chart().plotArea().contains(pos):
            chart_val = self.chart().mapToValue(pos)
            chart_ts = chart_val.x() / 1000.0

            closest_entry = min(self.results_data, key=lambda x: abs(x['timestamp'] - chart_ts))

            plot_area = self.chart().plotArea()
            self.chart().mapToPosition(chart_val)

            self.crosshair.setLine(pos.x(), plot_area.top(), pos.x(), plot_area.bottom())
            self.crosshair.show()

            dt = datetime.fromtimestamp(closest_entry['timestamp'])
            time_str = dt.strftime("%H:%M:%S")

            tooltip_lines = [f"<b><span style='color: #3C3C4C;'>Time: {time_str}</span></b>","<hr>"]
            for cat, config in self.category_config.items():
                val = closest_entry.get(cat, 0.0)
                color = config['color']
                tooltip_lines.append(f"<font color='{color}'>• {cat.capitalize()}: {val:.2f}%</font>")

            tooltip_pos = event.globalPosition().toPoint()
            tooltip_pos.setX(tooltip_pos.x() + 10)
            tooltip_pos.setY(tooltip_pos.y() + 10)

            QToolTip.showText(tooltip_pos, "<br>".join(tooltip_lines), self)
        else:
            self.crosshair.hide()
            QToolTip.hideText()

    def leaveEvent(self, event):
        self.crosshair.hide()
        super().leaveEvent(event)