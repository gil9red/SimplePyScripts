#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import calendar
import math
import sys
import time
import traceback

from datetime import datetime, date, timedelta

from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow,
    QSystemTrayIcon,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QSplitter,
    QLabel,
    QGridLayout,
    QHeaderView,
    QProgressBar,
    QMenu,
    QComboBox,
)
from PyQt5.QtGui import QIcon, QPainter, QCloseEvent
from PyQt5.QtCore import QEvent, QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtChart import QChart, QLineSeries, QDateTimeAxis, QValueAxis

from common import ROOT_DIR, DIR, get_table
from get_assigned_open_issues_per_project import get_assigned_open_issues_per_project
from db import Run

sys.path.append(str(ROOT_DIR.parent / "qt__pyqt__pyside__pyqode"))
from chart_line__show_tooltip_on_series__QtChart import ChartViewToolTips


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


WINDOW_TITLE: str = DIR.name

DATE_FORMAT: str = "%d.%m.%Y"
TIME_FORMAT: str = "%H:%M:%S"


def get_human_datetime(dt: datetime | None = None) -> str:
    if not dt:
        dt = datetime.now()
    return dt.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")


def get_human_date(d: datetime | date | None = None) -> str:
    if not d:
        d = date.today()
    return d.strftime(DATE_FORMAT)


def get_human_time(dt: datetime | None = None) -> str:
    if not dt:
        dt = datetime.now()
    return dt.strftime(TIME_FORMAT)


def get_table_widget(header_labels: list) -> QTableWidget:
    table = QTableWidget()
    table.setAlternatingRowColors(True)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setSelectionMode(QTableWidget.SingleSelection)
    table.setColumnCount(len(header_labels))
    table.setHorizontalHeaderLabels(header_labels)
    table.horizontalHeader().setStretchLastSection(True)
    return table


class GetAssignedOpenIssuesPerProjectThread(QThread):
    about_items = pyqtSignal(dict)
    about_error = pyqtSignal(Exception)

    def run(self):
        try:
            items: dict[str, int] = get_assigned_open_issues_per_project()
            self.about_items.emit(items)

            # Даем время на отображение и анимацию прогресс-бара
            time.sleep(0.3)

        except Exception as e:
            self.about_error.emit(e)


class TableWidgetRun(QWidget):
    def __init__(self):
        super().__init__()

        self.table_run = get_table_widget(["DATE", "TOTAL ISSUES"])
        self.table_run.selectionModel().selectionChanged.connect(
            self._on_table_run_item_clicked
        )

        self.table_issues = get_table_widget(["PROJECT", "NUMBER"])
        self.table_run.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_issues.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.table_run)
        splitter.addWidget(self.table_issues)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    def refresh(self, items: list[Run]):
        # Удаление строк таблицы
        while self.table_run.rowCount():
            self.table_run.removeRow(0)

        for i, run in enumerate(items):
            self.table_run.setRowCount(self.table_run.rowCount() + 1)

            item = QTableWidgetItem(get_human_date(run.date))
            item.setData(Qt.UserRole, run.get_project_by_issue_numbers())
            self.table_run.setItem(i, 0, item)

            item = QTableWidgetItem(str(run.get_total_issues()))
            self.table_run.setItem(i, 1, item)

        self.table_run.setCurrentCell(0, 0)
        self.table_run.setFocus()
        self._on_table_run_item_clicked()

    def _on_table_run_item_clicked(self):
        # Удаление строк таблицы
        while self.table_issues.rowCount():
            self.table_issues.removeRow(0)

        item = self.table_run.item(self.table_run.currentRow(), 0)
        if not item:
            return

        for i, (project_name, number) in enumerate(item.data(Qt.UserRole).items()):
            self.table_issues.setRowCount(self.table_issues.rowCount() + 1)

            self.table_issues.setItem(i, 0, QTableWidgetItem(project_name))
            self.table_issues.setItem(i, 1, QTableWidgetItem(str(number)))


class CurrentAssignedOpenIssues(QWidget):
    def __init__(self):
        super().__init__()

        self.table = get_table_widget(["PROJECT", "NUMBER"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        sp_progress_bar = self.progress_bar.sizePolicy()
        sp_progress_bar.setRetainSizeWhenHidden(True)
        self.progress_bar.setSizePolicy(sp_progress_bar)
        self.progress_bar.hide()

        self.label_total = QLabel()
        font = self.label_total.font()
        font.setPixelSize(30)
        self.label_total.setFont(font)

        self.label_last_refresh_date = QLabel()
        font = self.label_last_refresh_date.font()
        font.setPixelSize(18)
        self.label_last_refresh_date.setFont(font)

        main_layout = QGridLayout()
        main_layout.addWidget(self.label_total, 0, 0, Qt.AlignLeft | Qt.AlignCenter)
        main_layout.addWidget(self.progress_bar, 0, 1)
        main_layout.addWidget(
            self.label_last_refresh_date, 0, 2, Qt.AlignRight | Qt.AlignCenter
        )
        main_layout.addWidget(self.table, 1, 0, 2, 0)

        self.setLayout(main_layout)

        self.thread = GetAssignedOpenIssuesPerProjectThread()
        self.thread.started.connect(self.progress_bar.show)
        self.thread.finished.connect(self.progress_bar.hide)
        self.thread.about_items.connect(self._on_set_items)
        self.thread.about_error.connect(self._on_error)

        self.current_items: dict[str, int] | None = None
        self._update_total_issues("-")

    def _update_total_issues(self, value):
        self.label_total.setText(f"<b>Total issues:</b> {value}")

    def _on_set_items(self, items: dict[str, int]):
        self.current_items = items

        self._update_total_issues(sum(self.current_items.values()))

        # Удаление строк таблицы
        while self.table.rowCount():
            self.table.removeRow(0)

        for i, (project_name, number) in enumerate(self.current_items.items()):
            self.table.setRowCount(self.table.rowCount() + 1)

            self.table.setItem(i, 0, QTableWidgetItem(project_name))
            self.table.setItem(i, 1, QTableWidgetItem(str(number)))

        self.label_last_refresh_date.setText(
            f"Last refresh date: {get_human_datetime()}"
        )

    def _on_error(self, e: Exception):
        tb_str = "".join(traceback.format_tb(e.__traceback__))
        print(tb_str)
        QMessageBox.warning(self, "ERROR", str(e))

    def refresh(self):
        self.current_items = None

        self.thread.start()


class MyChartViewToolTips(ChartViewToolTips):
    def __init__(self, timestamp_by_info: dict[int, dict[str, int]]):
        super().__init__()

        self._callout_font_family = "Courier"
        self.timestamp_by_info: dict[int, dict[str, int]] = timestamp_by_info

    def show_series_tooltip(self, point, state: bool):
        # value -> pos
        point = self.chart().mapToPosition(point)

        if not self._tooltip:
            self._tooltip = self._add_Callout()

        if not state:
            self._tooltip.hide()
            return

        distance = 25

        for series in self.chart().series():
            for p_value in series.pointsVector():
                p = self.chart().mapToPosition(p_value)

                current_distance = math.sqrt(
                    (p.x() - point.x()) * (p.x() - point.x())
                    + (p.y() - point.y()) * (p.y() - point.y())
                )

                if current_distance < distance:
                    time_ms = int(p_value.x())
                    info: dict[str, int] = self.timestamp_by_info[time_ms]
                    table = get_table(info)
                    text = (
                        f"{get_human_date(date.fromtimestamp(time_ms / 1000))}"
                        "\n\n"
                        f"Total issues: {sum(info.values())}"
                        "\n"
                        f"{table}"
                    )

                    self._tooltip.setText(text)
                    self._tooltip.setAnchor(p_value)
                    self._tooltip.setZValue(11)
                    self._tooltip.updateGeometry()
                    self._tooltip.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)

        file_name = str(DIR / "favicon.ico")
        icon = QIcon(file_name)
        self.setWindowIcon(icon)

        self.timestamp_by_info: dict[int, dict[str, int]] = dict()

        menu = QMenu()
        menu.addAction("Show / hide", (lambda: self.setVisible(not self.isVisible())))
        menu.addSeparator()
        menu.addAction("Quit", QApplication.instance().quit)

        self.tray = QSystemTrayIcon(icon)
        self.tray.setContextMenu(menu)
        self.tray.setToolTip(self.windowTitle())
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

        self.chart_view = MyChartViewToolTips(self.timestamp_by_info)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.cb_chart_filter = QComboBox()
        self.cb_chart_filter.addItem("<all years>", userData=0)
        self.cb_chart_filter.activated.connect(self.refresh)
        layout_chart_view = QVBoxLayout(self.chart_view)
        layout_chart_view.addWidget(self.cb_chart_filter)
        layout_chart_view.setAlignment(
            self.cb_chart_filter, Qt.AlignTop | Qt.AlignRight
        )

        self.table_run = TableWidgetRun()
        self.table_run.layout().setContentsMargins(0, 0, 0, 0)

        self.current_assigned_open_issues = CurrentAssignedOpenIssues()

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.chart_view, "CHART")
        self.tab_widget.addTab(self.table_run, "TABLE RUN")
        self.tab_widget.addTab(
            self.current_assigned_open_issues, "Current Assigned Open Issues"
        )

        self.pb_refresh = QPushButton("REFRESH")
        self.pb_refresh.clicked.connect(self.refresh)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.pb_refresh)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    @staticmethod
    def _get_timegm(date: date) -> int:
        return calendar.timegm(date.timetuple()) * 1000

    def _get_datetime(self, date: date, delta: timedelta = None) -> datetime:
        dt = datetime.combine(date, datetime.min.time())
        if delta:
            dt += delta
        return dt

    def _fill_chart_filter(self, items: list[Run]):
        years: list[int] = sorted({run.date.year for run in items})
        filter_years: list[int] = [
            self.cb_chart_filter.itemData(i)
            for i in range(self.cb_chart_filter.count())
        ]
        for year in years:
            if year not in filter_years:
                self.cb_chart_filter.addItem(f"{year}", userData=year)

    def _fill_chart(self, items: list[Run]):
        # Фильтрация данных из графика
        year: int = self.cb_chart_filter.currentData()
        if year:
            items = [run for run in items if run.date.year == year]

        series = QLineSeries()
        series.setPointsVisible(True)
        series.setPointLabelsVisible(True)
        series.setPointLabelsFormat("@yPoint")
        series.hovered.connect(self.chart_view.show_series_tooltip)

        self.timestamp_by_info.clear()

        issues_number = []
        for run in items:
            date_value = self._get_timegm(run.date)
            total_issues = run.get_total_issues()
            series.append(date_value, total_issues)
            issues_number.append(total_issues)

            self.timestamp_by_info[date_value] = run.get_project_by_issue_numbers()

        now_date_timestamp = self._get_timegm(date.today())
        if now_date_timestamp not in self.timestamp_by_info:
            # Использование данных из соседнего виджета
            self.current_assigned_open_issues.refresh()
            while not self.current_assigned_open_issues.current_items:
                QApplication.instance().processEvents()

            self.timestamp_by_info[now_date_timestamp] = self.current_assigned_open_issues.current_items
            series.append(now_date_timestamp, sum(self.current_assigned_open_issues.current_items.values()))

        chart = QChart()
        chart.setTheme(QChart.ChartThemeDark)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.addSeries(series)
        chart.legend().hide()

        # No margin
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        axisX = QDateTimeAxis()
        if items:
            axisX.setRange(
                self._get_datetime(items[0].date, timedelta(days=-30)),
                self._get_datetime(items[-1].date, timedelta(days=30)),
            )
        axisX.setFormat("dd/MM/yyyy")
        axisX.setTitleText("Date")
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        if issues_number:
            axisY.setRange(min(issues_number) * 0.8, max(issues_number) * 1.2)
        axisY.setLabelFormat("%d")
        axisY.setTitleText("Total issues")
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.chart_view.clear_all_tooltips()
        self.chart_view.setChart(chart)

    def refresh(self):
        self.current_assigned_open_issues.refresh()

        items = list(Run.select())

        self._fill_chart_filter(items)

        self._fill_chart(items)

        items.reverse()
        self.table_run.refresh(items)

        self.setWindowTitle(
            f"{WINDOW_TITLE}. Last refresh date: {get_human_datetime()}"
        )

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason):
        # Если запрошено меню
        if reason == QSystemTrayIcon.Context:
            return

        self.setVisible(not self.isVisible())

        if self.isVisible():
            self.showNormal()
            self.activateWindow()

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.WindowStateChange:
            # Если окно свернули
            if self.isMinimized():
                # Прячем окно с панели задач
                QTimer.singleShot(0, self.hide)

    def closeEvent(self, event: QCloseEvent):
        self.hide()
        event.ignore()


if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    mw = MainWindow()
    mw.resize(1200, 800)
    mw.show()

    mw.refresh()

    app.exec()
