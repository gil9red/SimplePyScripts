#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import math

from PyQt5.QtWidgets import QApplication
from PyQt5.QtChart import QChart, QLineSeries

from chart_line__show_tooltip_on_series__QtChart import Callout, ChartViewToolTips


class MainWindow(ChartViewToolTips):
    def __init__(self) -> None:
        super().__init__()

        series = QLineSeries()
        series.setPointsVisible(True)
        series.setPointLabelsVisible(True)
        series.setPointLabelsFormat("(@xPoint, @yPoint)")
        series.hovered.connect(self.show_series_tooltip)

        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)

        self._chart = QChart()
        self._chart.setMinimumSize(640, 480)
        self._chart.setTitle("Line Chart Example")
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        self._chart.legend().hide()
        self._chart.addSeries(series)
        self._chart.createDefaultAxes()

        self.setChart(self._chart)

    def show_series_tooltip(self, point, state: bool) -> None:
        # value -> pos
        point = self._chart.mapToPosition(point)

        if not self._tooltip:
            self._tooltip = Callout(self._chart)

        if state:
            distance = 20
            for series in self._chart.series():
                for p_value in series.pointsVector():
                    p = self._chart.mapToPosition(p_value)

                    current_distance = math.sqrt(
                        (p.x() - point.x()) * (p.x() - point.x())
                        + (p.y() - point.y()) * (p.y() - point.y())
                    )
                    if current_distance < distance:
                        self._tooltip.setText(f"X: {p.x()}\nY: {p.y()}")
                        self._tooltip.setAnchor(p_value)
                        self._tooltip.setZValue(11)
                        self._tooltip.updateGeometry()
                        self._tooltip.show()
        else:
            self._tooltip.hide()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.setWindowTitle("Chart Line")
    mw.resize(800, 600)
    mw.show()

    app.exec()
