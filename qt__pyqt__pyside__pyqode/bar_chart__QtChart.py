#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random

from PyQt5.QtGui import QPainter
from PyQt5.Qt import *
from PyQt5.QtChart import *


class MainWidow(QMainWindow):
    def __init__(self):
        super().__init__()

        series = self.append_series()

        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chart.addSeries(series)
        self.chart.setTitle("Simple percent barchart example")

        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chart_view)

    def append_series(self):
        set0 = QBarSet("Min")
        set1 = QBarSet("Mid")
        set2 = QBarSet("Max")

        set0.append([random.randint(0, 10) for _ in range(5)])
        set1.append([random.randint(0, 10) for _ in range(5)])
        set2.append([random.randint(0, 10) for _ in range(5)])

        series = QStackedBarSeries()

        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.setBarWidth(1)

        return series


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    mw = MainWidow()
    mw.resize(800, 500)
    mw.show()

    sys.exit(app.exec_())
