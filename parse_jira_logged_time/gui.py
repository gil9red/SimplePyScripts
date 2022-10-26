#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import io
import sys
import traceback
import webbrowser

from contextlib import redirect_stdout
from datetime import datetime

from PyQt5.Qt import (
    QApplication, QMessageBox, QThread, pyqtSignal, QMainWindow, QPushButton, QCheckBox, QPlainTextEdit,
    QVBoxLayout, QHBoxLayout, QTextOption, QTableWidget, QWidget, QSizePolicy, QSplitter, Qt, QTableWidgetItem,
    QProgressDialog, QHeaderView, QSystemTrayIcon, QIcon, QEvent, QTimer
)

from main import (
    DIR, get_rss_jira_log, parse_logged_dict, get_logged_list_by_now_utc_date, get_logged_total_seconds,
    get_sorted_logged, seconds_to_str
)


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f'{ex_cls.__name__}: {ex}:\n'
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class RunFuncThread(QThread):
    run_finished = pyqtSignal(object)

    def __init__(self, func):
        super().__init__()

        self.func = func

    def run(self):
        self.run_finished.emit(self.func())


WINDOW_TITLE = 'parse_jira_logged_time'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)

        file_name = str(DIR / 'favicon.ico')
        icon = QIcon(file_name)

        self.setWindowIcon(icon)

        self.tray = QSystemTrayIcon(icon)
        self.tray.setToolTip(self.windowTitle())
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

        self.logged_dict = dict()

        self.pb_refresh = QPushButton('REFRESH')
        self.pb_refresh.clicked.connect(self.refresh)

        self.cb_show_log = QCheckBox()
        self.cb_show_log.setChecked(True)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setWordWrapMode(QTextOption.NoWrap)
        log_font = self.log.font()
        log_font.setFamily('Courier New')
        self.log.setFont(log_font)

        self.cb_show_log.clicked.connect(self.log.setVisible)
        self.log.setVisible(self.cb_show_log.isChecked())

        header_labels = ['DATE', 'TOTAL LOGGED TIME']
        self.table_logged = QTableWidget()
        self.table_logged.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_logged.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_logged.setSelectionMode(QTableWidget.SingleSelection)
        self.table_logged.setColumnCount(len(header_labels))
        self.table_logged.setHorizontalHeaderLabels(header_labels)
        self.table_logged.horizontalHeader().setStretchLastSection(True)
        self.table_logged.itemClicked.connect(self._on_table_logged_item_clicked)

        header_labels = ['TIME', 'LOGGED', 'JIRA']
        self.table_logged_info = QTableWidget()
        self.table_logged_info.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_logged_info.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_logged_info.setSelectionMode(QTableWidget.SingleSelection)
        self.table_logged_info.setColumnCount(len(header_labels))
        self.table_logged_info.setHorizontalHeaderLabels(header_labels)
        self.table_logged_info.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_logged_info.horizontalHeader().setStretchLastSection(True)
        self.table_logged_info.itemDoubleClicked.connect(self._on_table_logged_info_item_double_clicked)

        main_layout = QVBoxLayout()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

        self.pb_refresh.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.pb_refresh)
        h_layout.addWidget(self.cb_show_log)

        layout_table_widget = QVBoxLayout()
        layout_table_widget.setContentsMargins(0, 0, 0, 0)
        layout_table_widget.addWidget(self.table_logged)
        layout_table_widget.addWidget(self.table_logged_info)

        table_widget = QWidget()
        table_widget.setLayout(layout_table_widget)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(table_widget)
        splitter.addWidget(self.log)

        main_layout.addLayout(h_layout)
        main_layout.addWidget(splitter)

    def _fill_tables(self, xml_data: bytes):
        buffer_io = io.StringIO()
        try:
            with redirect_stdout(buffer_io):
                print(len(xml_data), repr(xml_data[:50]))

                # Структура документа -- xml
                self.logged_dict = parse_logged_dict(xml_data)
                print(self.logged_dict)

                if not self.logged_dict:
                    return

                print(json.dumps(self.logged_dict, indent=4, ensure_ascii=False))
                print()

                logged_list = get_logged_list_by_now_utc_date(self.logged_dict)

                logged_total_seconds = get_logged_total_seconds(logged_list)
                logged_total_seconds_str = seconds_to_str(logged_total_seconds)
                print('entry_logged_list:', logged_list)
                print('today seconds:', logged_total_seconds)
                print('today time:', logged_total_seconds_str)
                print()

                # Для красоты выводим результат в табличном виде
                lines = []

                # Удаление строк таблицы
                while self.table_logged.rowCount():
                    self.table_logged.removeRow(0)

                for i, (date_str, logged_list) in enumerate(get_sorted_logged(self.logged_dict)):
                    total_seconds = get_logged_total_seconds(logged_list)
                    total_seconds_str = seconds_to_str(total_seconds)
                    row = date_str, total_seconds_str, total_seconds
                    lines.append(row)

                    self.table_logged.setRowCount(self.table_logged.rowCount() + 1)

                    self.table_logged.setItem(i, 0, QTableWidgetItem(date_str))

                    item = QTableWidgetItem(total_seconds_str)
                    item.setToolTip('Total seconds: {}'.format(total_seconds))
                    self.table_logged.setItem(i, 1, item)

                self.table_logged.setCurrentCell(0, 0)
                self.table_logged.setFocus()
                self._on_table_logged_item_clicked(self.table_logged.currentItem())

                # Список строк станет списком столбцов, у каждого столбца подсчитается максимальная длина
                max_len_columns = [max(map(len, map(str, col))) for col in zip(*lines)]

                # Создание строки форматирования: [30, 14, 5] -> "{:<30} | {:<14} | {:<5}"
                my_table_format = ' | '.join('{:<%s}' % max_len for max_len in max_len_columns)

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

        progress_dialog.setWindowTitle('Please wait...')
        progress_dialog.setLabelText(progress_dialog.windowTitle())
        progress_dialog.setRange(0, 0)
        progress_dialog.exec()

        self.setWindowTitle(WINDOW_TITLE + ". Last refresh date: " + datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    def _on_table_logged_item_clicked(self, item: QTableWidgetItem):
        # Удаление строк таблицы
        while self.table_logged_info.rowCount():
            self.table_logged_info.removeRow(0)

        row = item.row()
        date_str = self.table_logged.item(row, 0).text()
        logged_list = self.logged_dict[date_str]
        logged_list = reversed(logged_list)

        for i, logged in enumerate(logged_list):
            self.table_logged_info.setRowCount(self.table_logged_info.rowCount() + 1)

            self.table_logged_info.setItem(i, 0, QTableWidgetItem(logged['time']))
            self.table_logged_info.setItem(i, 1, QTableWidgetItem(logged['logged_human_time']))

            item = QTableWidgetItem(logged['jira_id'])
            item.setToolTip(logged['jira_title'])
            self.table_logged_info.setItem(i, 2, item)

    def _on_table_logged_info_item_double_clicked(self, item: QTableWidgetItem):
        row = item.row()
        jira_id = self.table_logged_info.item(row, 2).text()

        url = 'https://helpdesk.compassluxe.com/browse/' + jira_id
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


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(1200, 800)
    mw.show()

    mw.refresh()

    app.exec()
