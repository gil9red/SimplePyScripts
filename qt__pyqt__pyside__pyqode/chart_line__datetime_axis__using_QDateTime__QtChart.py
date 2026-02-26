#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://doc.qt.io/qt-5/qtcharts-datetimeaxis-example.html


from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PyQt5.QtCore import QDateTime, Qt


DATA = [
    ((2012, 1, 18), 20),
    ((2012, 2, 1), 22),
    ((2012, 3, 4), 18),
    ((2012, 8, 7), 5),
    ((2013, 2, 19), 6),
    ((2016, 2, 19), 35),
]


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        series = QLineSeries()

        for date, value in DATA:
            date_value = QDateTime(*date, 0, 0).toMSecsSinceEpoch()
            series.append(date_value, value)

        chart = QChart()
        chart.setTheme(QChart.ChartThemeDark)
        chart.setTitle("Line Chart with Date Example")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.addSeries(series)
        chart.legend().hide()

        axisX = QDateTimeAxis()
        axisX.setFormat("dd/MM/yyyy")
        axisX.setTitleText("Date")
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("Value")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        chart_view = QChartView()
        chart_view.setChart(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chart_view)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.setWindowTitle("Line Chart with Date Example. QDateTime")
    mw.resize(800, 600)
    mw.show()

    app.exec()
