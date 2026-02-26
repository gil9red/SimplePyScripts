#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        series = QLineSeries()
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)

        chart = QChart()
        chart.setTitle("Dark Theme")
        chart.setTheme(QChart.ChartThemeDark)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()

        chart_view = QChartView()
        chart_view.setChart(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chart_view)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.setWindowTitle("Chart Line")
    mw.resize(800, 600)
    mw.show()

    app.exec()
