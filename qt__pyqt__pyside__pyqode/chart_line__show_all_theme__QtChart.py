#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries


def get_themes() -> list[tuple[str, QChart.ChartTheme]]:
    NAME = "ChartTheme"

    themes = []
    for theme_name in dir(QChart):
        if theme_name == NAME or not theme_name.startswith(NAME):
            continue

        theme = getattr(QChart, theme_name)
        theme_name = theme_name.replace(NAME, "")

        themes.append((theme_name, theme))

    themes.sort(key=lambda x: x[1])
    return themes


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        tab_widget = QTabWidget()

        chart_view = self.create_QChartView()
        tab_widget.addTab(chart_view, "<DEFAULT>")

        for name, theme in get_themes():
            chart_view = self.create_QChartView()
            chart_view.chart().setTheme(theme)

            tab_widget.addTab(chart_view, name)

        self.setCentralWidget(tab_widget)

    def create_QChartView(self) -> QChartView:
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

    mw = MainWindow()
    mw.setWindowTitle("Show All Themes")
    mw.resize(800, 600)
    mw.show()

    app.exec()
