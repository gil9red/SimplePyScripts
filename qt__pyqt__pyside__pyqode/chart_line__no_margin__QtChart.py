#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries


def create_QChartView() -> QChartView:
    series = QLineSeries()
    series.append(0, 6)
    series.append(2, 4)
    series.append(3, 8)
    series.append(7, 4)
    series.append(10, 5)

    chart = QChart()
    chart.setTitle("Line Chart Example")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().hide()
    chart.addSeries(series)
    chart.createDefaultAxes()

    chart_view = QChartView()
    chart_view.setChart(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)

    return chart_view


if __name__ == "__main__":
    app = QApplication([])

    mw = create_QChartView()
    mw.setWindowTitle("No margin")
    mw.chart().setTheme(QChart.ChartThemeDark)

    # No margin
    mw.chart().layout().setContentsMargins(0, 0, 0, 0)
    mw.chart().setBackgroundRoundness(0)

    mw.resize(800, 600)
    mw.show()

    app.exec()
