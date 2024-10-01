#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import io
import sys
import traceback
import webbrowser

from contextlib import redirect_stdout
from datetime import datetime, date
from typing import Any

from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow,
    QPushButton,
    QCheckBox,
    QPlainTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QWidget,
    QSplitter,
    QTableWidgetItem,
    QHeaderView,
    QSystemTrayIcon,
    QProgressBar,
    QSizePolicy,
    QToolTip,
)
from PyQt5.QtCore import (
    QThread,
    pyqtSignal,
    Qt,
    QEvent,
    QTimer,
)
from PyQt5.QtGui import QTextOption, QIcon

from config import PATH_FAVICON, JIRA_HOST, USERNAME
from console import (
    URL,
    Activity,
    get_rss_jira_log,
    seconds_to_str,
    parse_date_by_activities,
    get_logged_total_seconds,
)


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class RunFuncThread(QThread):
    run_finished = pyqtSignal(object)
    about_error = pyqtSignal(str)

    def __init__(self, func):
        super().__init__()

        self.func = func

    def run(self):
        try:
            self.run_finished.emit(self.func())
        except Exception as e:
            print(f"Error: {e}")
            self.about_error.emit(traceback.format_exc())


WINDOW_TITLE: str = f"parse_jira_logged_time. {USERNAME}"


def create_table(header_labels: list[str]) -> QTableWidget:
    table_widget = QTableWidget()
    table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
    table_widget.setSelectionBehavior(QTableWidget.SelectRows)
    table_widget.setSelectionMode(QTableWidget.SingleSelection)
    table_widget.setColumnCount(len(header_labels))
    table_widget.setHorizontalHeaderLabels(header_labels)
    table_widget.horizontalHeader().setStretchLastSection(True)

    return table_widget


def create_table_item(
    text: str,
    tool_tip: str | None = None,
    data: Any = None,
) -> QTableWidgetItem:
    item = QTableWidgetItem(text)

    if tool_tip:
        item.setToolTip(tool_tip)

    if data:
        item.setData(Qt.UserRole, data)

    return item


def clear_table(table_widget: QTableWidget):
    # Удаление строк таблицы
    while table_widget.rowCount():
        table_widget.removeRow(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)

        icon = QIcon(str(PATH_FAVICON))

        self.setWindowIcon(icon)

        self.tray = QSystemTrayIcon(icon)
        self.tray.setToolTip(self.windowTitle())
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

        self.pb_refresh = QPushButton("🔄 REFRESH")
        self.pb_refresh.setObjectName("pb_refresh")
        self.pb_refresh.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.pb_refresh.clicked.connect(self.refresh)

        self.progress_refresh = QProgressBar()
        self.progress_refresh.setObjectName("progress_refresh")
        self.progress_refresh.setRange(0, 0)
        self.progress_refresh.setTextVisible(False)
        self.progress_refresh.hide()

        self.cb_show_log = QCheckBox()
        self.cb_show_log.setText("Show log")
        self.cb_show_log.setChecked(False)

        self.timer_auto_refresh = QTimer()
        self.timer_auto_refresh.setInterval(60 * 60 * 1000)  # 1 hour
        self.timer_auto_refresh.timeout.connect(self.refresh)

        self.cb_auto_refresh = QCheckBox()
        self.cb_auto_refresh.setText("Auto")
        self.cb_auto_refresh.setToolTip("Every 1 hour")
        self.cb_auto_refresh.setChecked(True)

        self.cb_auto_refresh.clicked.connect(self.set_auto_refresh)
        if self.cb_auto_refresh.isChecked():
            self.timer_auto_refresh.start()

        self.log = QPlainTextEdit()
        self.log.setObjectName("log")
        self.log.setReadOnly(True)
        self.log.setWordWrapMode(QTextOption.NoWrap)

        self.cb_show_log.clicked.connect(self.log.setVisible)
        self.log.setVisible(self.cb_show_log.isChecked())

        self.thread_get_data = RunFuncThread(func=get_rss_jira_log)
        self.thread_get_data.started.connect(self._before_refresh)
        self.thread_get_data.about_error.connect(self._set_error_log)
        self.thread_get_data.run_finished.connect(self._fill_tables)
        self.thread_get_data.finished.connect(self._after_refresh)

        self.table_logged = create_table(
            header_labels=["DATE", "TOTAL LOGGED TIME"],
        )
        self.table_logged.itemSelectionChanged.connect(
            lambda: self._on_table_logged_item_clicked(self.table_logged.currentItem())
        )

        self.table_logged_info = create_table(
            header_labels=["TIME", "LOGGED", "JIRA", "TITLE"],
        )

        # Первые 3 колонки (кроме названия) имеют размер под содержимое
        for j in range(3):
            self.table_logged_info.horizontalHeader().setSectionResizeMode(
                j, QHeaderView.ResizeToContents
            )
        self.table_logged_info.itemDoubleClicked.connect(
            self._on_table_logged_info_item_double_clicked
        )

        splitter_table = QSplitter(Qt.Horizontal)
        splitter_table.addWidget(self.table_logged)
        splitter_table.addWidget(self.table_logged_info)
        splitter_table.setSizes([300, 600])

        layout_log = QVBoxLayout()
        layout_log.addWidget(self.log)
        layout_log.addWidget(self.cb_show_log)

        layout_content = QVBoxLayout()
        layout_content.addWidget(splitter_table)
        layout_content.addLayout(layout_log)

        layout_refresh = QHBoxLayout()
        layout_refresh.addWidget(self.pb_refresh)
        layout_refresh.addWidget(self.cb_auto_refresh)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_refresh)
        layout_main.addWidget(self.progress_refresh)
        layout_main.addLayout(layout_content)

        central_widget = QWidget()
        central_widget.setLayout(layout_main)

        self.setCentralWidget(central_widget)

        self.setStyleSheet(
            """
            * {
                font-size: 16px;
            }
            #pb_refresh {
                font-size: 18px;
            }
            #progress_refresh {
                min-height: 14px;
                max-height: 14px;
            }
            #log {
                font-family: Courier New;
            }
            """
        )

    def set_auto_refresh(self, checked: bool):
        if checked:
            self.timer_auto_refresh.start()
        else:
            self.timer_auto_refresh.stop()

        pos = self.cb_auto_refresh.geometry().topRight()
        pos = self.mapToGlobal(pos)
        QToolTip.showText(pos, f"Timer {'started' if checked else 'stopped'}")

    def _set_error_log(self, text: str):
        self.log.setPlainText(text)

        # Отображение лога
        self.cb_show_log.setChecked(False)
        self.cb_show_log.click()

    def _fill_tables(self, xml_data: bytes):
        buffer_io = io.StringIO()
        try:
            print(f"{URL}\n")

            with redirect_stdout(buffer_io):
                print(
                    f"Xml data ({len(xml_data)} bytes):\n"
                    f"{xml_data[:150] + b'...' if len(xml_data) > 150 else xml_data!r}"
                )

                date_by_activities: dict[
                    date, list[Activity]
                ] = parse_date_by_activities(xml_data)
                if not date_by_activities:
                    return

                # Для красоты выводим результат в табличном виде
                table_header: tuple = ("DATE", "LOGGED", "SECONDS", "ACTIVITIES")
                table_lines: list[tuple[str, str, int, int]] = []

                clear_table(self.table_logged)

                for entry_date, activities in sorted(
                    date_by_activities.items(), key=lambda x: x[0], reverse=True
                ):
                    activities_number = len(activities)

                    activities: list[Activity] = [
                        obj for obj in reversed(activities) if obj.is_logged()
                    ]

                    total_seconds: int = get_logged_total_seconds(activities)
                    total_seconds_str: str = seconds_to_str(total_seconds)

                    date_str: str = entry_date.strftime("%d/%m/%Y")
                    table_lines.append(
                        (date_str, total_seconds_str, total_seconds, activities_number)
                    )

                    is_odd_week: int = entry_date.isocalendar().week % 2 == 1

                    # Не показывать даты, в которых не было залогировано
                    if not total_seconds:
                        continue

                    items = [
                        create_table_item(date_str, data=activities),
                        create_table_item(
                            total_seconds_str,
                            tool_tip=f"Total seconds: {total_seconds}",
                        ),
                    ]

                    i = self.table_logged.rowCount()
                    self.table_logged.setRowCount(i + 1)
                    for j, item in enumerate(items):
                        if is_odd_week:
                            item.setBackground(Qt.lightGray)

                        self.table_logged.setItem(i, j, item)

                self.table_logged.setCurrentCell(0, 0)
                self.table_logged.setFocus()
                self._on_table_logged_item_clicked(self.table_logged.currentItem())

                print()

                # Список строк станет списком столбцов, у каждого столбца подсчитается максимальная длина
                table: list = [table_header] + table_lines
                max_len_columns = [max(map(len, map(str, col))) for col in zip(*table)]

                # Создание строки форматирования: [30, 14, 5] -> "{:<30} | {:<14} | {:<5}"
                my_table_format = " | ".join(
                    "{:<%s}" % max_len for max_len in max_len_columns
                )
                for line in table:
                    print(my_table_format.format(*line))

        finally:
            text = buffer_io.getvalue()
            self.log.setPlainText(text)

            print(text)

    def _before_refresh(self):
        self.pb_refresh.setEnabled(False)
        self.progress_refresh.show()

    def _after_refresh(self):
        self.pb_refresh.setEnabled(True)
        self.progress_refresh.hide()

        self.setWindowTitle(
            f"{WINDOW_TITLE}. Last refresh date: {datetime.now():%d/%m/%Y %H:%M:%S}"
        )
        self.tray.setToolTip(self.windowTitle())

    def refresh(self):
        # Если обновление уже запущено
        if self.thread_get_data.isRunning():
            return

        self.thread_get_data.start()

    def _on_table_logged_item_clicked(self, item: QTableWidgetItem | None):
        clear_table(self.table_logged_info)

        if not item:
            return

        row = item.row()
        item1 = self.table_logged.item(row, 0)

        activities: list[Activity] = item1.data(Qt.UserRole)
        if not activities:
            return

        for activity in activities:
            items = [
                create_table_item(activity.entry_dt.strftime("%H:%M:%S")),
                create_table_item(activity.logged_human_time),
                create_table_item(activity.jira_id),
                create_table_item(activity.jira_title, tool_tip=activity.jira_title),
            ]

            i = self.table_logged_info.rowCount()
            self.table_logged_info.setRowCount(i + 1)
            for j, item in enumerate(items):
                self.table_logged_info.setItem(i, j, item)

    def _on_table_logged_info_item_double_clicked(self, item: QTableWidgetItem):
        row = item.row()
        jira_id = self.table_logged_info.item(row, 2).text()

        url = f"{JIRA_HOST}/browse/{jira_id}"
        webbrowser.open(url)

    def _on_tray_activated(self, reason):
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


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(1200, 800)
    mw.show()

    mw.refresh()

    app.exec()
