#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import io
import sys
import traceback
import webbrowser

from contextlib import redirect_stdout
from datetime import datetime

from PyQt5.Qt import (
    QApplication,
    QMessageBox,
    QThread,
    pyqtSignal,
    QMainWindow,
    QPushButton,
    QCheckBox,
    QPlainTextEdit,
    QVBoxLayout,
    QTextOption,
    QTableWidget,
    QWidget,
    QSplitter,
    Qt,
    QTableWidgetItem,
    QProgressDialog,
    QHeaderView,
    QSystemTrayIcon,
    QIcon,
    QEvent,
    QTimer,
)

from config import PATH_FAVICON
from main import (
    get_rss_jira_log,
    parse_logged_dict,
    get_logged_list_by_now_utc_date,
    get_logged_total_seconds,
    get_sorted_logged,
    seconds_to_str,
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

    def __init__(self, func):
        super().__init__()

        self.func = func

    def run(self):
        self.run_finished.emit(self.func())


WINDOW_TITLE = "parse_jira_logged_time"


def create_table(header_labels: list[str]) -> QTableWidget:
    table_widget = QTableWidget()
    table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
    table_widget.setSelectionBehavior(QTableWidget.SelectRows)
    table_widget.setSelectionMode(QTableWidget.SingleSelection)
    table_widget.setColumnCount(len(header_labels))
    table_widget.setHorizontalHeaderLabels(header_labels)
    table_widget.horizontalHeader().setStretchLastSection(True)

    return table_widget


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
        self.pb_refresh.clicked.connect(self.refresh)

        self.cb_show_log = QCheckBox()
        self.cb_show_log.setText("Show log")
        self.cb_show_log.setChecked(False)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setWordWrapMode(QTextOption.NoWrap)
        log_font = self.log.font()
        log_font.setFamily("Courier New")
        self.log.setFont(log_font)

        self.cb_show_log.clicked.connect(self.log.setVisible)
        self.log.setVisible(self.cb_show_log.isChecked())

        self.table_logged = create_table(
            header_labels=["DATE", "TOTAL LOGGED TIME"],
        )
        self.table_logged.itemSelectionChanged.connect(
            lambda: self._on_table_logged_item_clicked(self.table_logged.currentItem())
        )

        self.table_logged_info = create_table(
            header_labels=["TIME", "LOGGED", "JIRA", "TITLE"],
        )
        self.table_logged_info.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.table_logged_info.itemDoubleClicked.connect(
            self._on_table_logged_info_item_double_clicked
        )

        splitter_table = QSplitter(Qt.Horizontal)
        splitter_table.addWidget(self.table_logged)
        splitter_table.addWidget(self.table_logged_info)
        splitter_table.setSizes([300, 600])

        layout_log = QVBoxLayout()
        layout_log.addWidget(self.cb_show_log)
        layout_log.addWidget(self.log)

        layout_content = QVBoxLayout()
        layout_content.addWidget(splitter_table)
        layout_content.addLayout(layout_log)

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.pb_refresh)
        layout_main.addLayout(layout_content)

        central_widget = QWidget()
        central_widget.setLayout(layout_main)

        self.setCentralWidget(central_widget)

    def _fill_tables(self, xml_data: bytes):
        buffer_io = io.StringIO()
        try:
            with redirect_stdout(buffer_io):
                print(
                    f"Xml data ({len(xml_data)} bytes):\n"
                    f"{xml_data[:150] + b'...' if len(xml_data) > 150 else xml_data!r}"
                )

                # Структура документа - xml
                logged_dict: dict[str, list[dict]] = parse_logged_dict(xml_data)
                print(logged_dict)

                if not logged_dict:
                    return

                print(json.dumps(logged_dict, indent=4, ensure_ascii=False))
                print()

                logged_list: list[dict] = get_logged_list_by_now_utc_date(logged_dict)

                logged_total_seconds = get_logged_total_seconds(logged_list)
                logged_total_seconds_str = seconds_to_str(logged_total_seconds)
                print("Entry_logged_list:", logged_list)
                print("Today seconds:", logged_total_seconds)
                print("Today time:", logged_total_seconds_str)
                print()

                # Для красоты выводим результат в табличном виде
                lines: list[tuple[str, str, int]] = []

                clear_table(self.table_logged)

                for i, (date_str, logged_list) in enumerate(
                    get_sorted_logged(logged_dict)
                ):
                    total_seconds = get_logged_total_seconds(logged_list)
                    total_seconds_str = seconds_to_str(total_seconds)
                    row = date_str, total_seconds_str, total_seconds
                    lines.append(row)

                    date: datetime = datetime.strptime(date_str, "%d/%m/%Y")
                    is_odd_week: int = date.isocalendar().week % 2 == 1

                    item1 = QTableWidgetItem(date_str)
                    item1.setData(Qt.UserRole, logged_list)

                    item2 = QTableWidgetItem(total_seconds_str)
                    item2.setToolTip(f"Total seconds: {total_seconds}")

                    self.table_logged.setRowCount(self.table_logged.rowCount() + 1)
                    for j, item in enumerate([item1, item2]):
                        if is_odd_week:
                            item.setBackground(Qt.lightGray)

                        self.table_logged.setItem(i, j, item)

                self.table_logged.setCurrentCell(0, 0)
                self.table_logged.setFocus()
                self._on_table_logged_item_clicked(self.table_logged.currentItem())

                # Список строк станет списком столбцов, у каждого столбца подсчитается максимальная длина
                max_len_columns = [max(map(len, map(str, col))) for col in zip(*lines)]

                # Создание строки форматирования: [30, 14, 5] -> "{:<30} | {:<14} | {:<5}"
                my_table_format = " | ".join(
                    "{:<%s}" % max_len for max_len in max_len_columns
                )

                for line in lines:
                    print(my_table_format.format(*line))

        finally:
            text = buffer_io.getvalue()
            self.log.setPlainText(text)

            print(text)

    def refresh(self):
        progress_dialog = QProgressDialog(self)

        thread = RunFuncThread(func=get_rss_jira_log)
        thread.run_finished.connect(self._fill_tables)
        thread.run_finished.connect(progress_dialog.close)
        thread.start()

        progress_dialog.setWindowTitle("Please wait...")
        progress_dialog.setLabelText(progress_dialog.windowTitle())
        progress_dialog.setRange(0, 0)
        progress_dialog.exec()

        self.setWindowTitle(
            f"{WINDOW_TITLE}. Last refresh date: {datetime.now():%d/%m/%Y %H:%M:%S}"
        )
        self.tray.setToolTip(self.windowTitle())

    def _on_table_logged_item_clicked(self, item: QTableWidgetItem):
        clear_table(self.table_logged_info)

        row = item.row()
        item1 = self.table_logged.item(row, 0)

        logged_list: list[dict] = item1.data(Qt.UserRole)

        for i, logged in enumerate(reversed(logged_list)):
            items = [
                QTableWidgetItem(logged["time"]),
                QTableWidgetItem(logged["logged_human_time"]),
                QTableWidgetItem(logged["jira_id"]),
                QTableWidgetItem(logged["jira_title"]),
            ]

            self.table_logged_info.setRowCount(self.table_logged_info.rowCount() + 1)
            for j, item in enumerate(items):
                self.table_logged_info.setItem(i, j, item)

    def _on_table_logged_info_item_double_clicked(self, item: QTableWidgetItem):
        row = item.row()
        jira_id = self.table_logged_info.item(row, 2).text()

        url = f"https://helpdesk.compassluxe.com/browse/{jira_id}"
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
