#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import sys
import time

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLabel,
    QCheckBox,
)
from PyQt5.QtCore import QThread, QTimer, QWaitCondition, QMutex, pyqtSignal, Qt


def get_pretty_int(num: int) -> str:
    return f"{num:,}".replace(",", " ")


class Thread(QThread):
    about_pause = pyqtSignal(bool)
    about_sum = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._is_pause = False
        self.condition = QWaitCondition()
        self.mutex = QMutex()
        self._sum = 0

    @property
    def sum(self) -> int:
        return self._sum

    @sum.setter
    def sum(self, value: int):
        self._sum = value
        self.about_sum.emit(value)

    def get_state(self) -> str:
        return "PAUSED" if self._is_pause else "WORKING"

    def set_pause(self, pause: bool):
        self._is_pause = pause
        self.about_pause.emit(pause)

        if not pause:
            self.condition.wakeAll()

    def is_pause(self) -> bool:
        return self._is_pause

    def pause(self):
        self.set_pause(True)

    def resume(self):
        self.set_pause(False)

    def run(self):
        while True:
            self.mutex.lock()
            if self._is_pause:
                self.condition.wait(self.mutex)
            self.sum += 1
            time.sleep(2)
            self.mutex.unlock()


class MainWindow(QWidget):
    headers = ["NAME", "STATE", "SUM"]

    def __init__(self):
        super().__init__()

        self.started: dt.datetime = None
        self._sum = 0

        self.table_thread = QTableWidget()
        self.table_thread.setColumnCount(len(self.headers))
        self.table_thread.setHorizontalHeaderLabels(self.headers)
        self.table_thread.horizontalHeader().setStretchLastSection(True)
        self.table_thread.setAlternatingRowColors(True)
        self.table_thread.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_thread.setSelectionMode(QTableWidget.SingleSelection)
        self.table_thread.setMinimumHeight(250)
        self.table_thread.selectionModel().currentRowChanged.connect(
            self._update_states
        )

        self.label_result = QLabel()

        self.button_add = QPushButton("Add")
        self.button_add.clicked.connect(self.add)

        self.button_pause = QPushButton("Pause")
        self.button_pause.clicked.connect(self.pause)

        self.button_pause_all = QPushButton("Pause all")
        self.button_pause_all.clicked.connect(self.pause_all)

        self.button_resume = QPushButton("Resume")
        self.button_resume.clicked.connect(self.resume)

        self.button_resume_all = QPushButton("Resume all")
        self.button_resume_all.clicked.connect(self.resume_all)

        self.cb_reset_sum = QCheckBox("Reset sum")
        self.cb_reset_sum.setChecked(True)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.table_thread)
        left_layout.addWidget(self.label_result)

        right_layout = QGridLayout()
        right_layout.addWidget(self.button_add, 0, 0, 1, 2)
        right_layout.addWidget(self.button_pause, 1, 0)
        right_layout.addWidget(self.button_pause_all, 1, 1)
        right_layout.addWidget(self.button_resume, 2, 0)
        right_layout.addWidget(self.button_resume_all, 2, 1)
        right_layout.addWidget(self.cb_reset_sum, 3, 0, 1, 2)
        right_layout.setRowStretch(right_layout.rowCount(), 1)

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)

        self._update_states()

    def _update_window_title(self):
        threads_num = self.table_thread.rowCount()
        if self.started:
            elapsed = str(dt.datetime.now() - self.started).split(".")[0]
            self.setWindowTitle(f"Threads: {threads_num}. Elapsed: {elapsed}")
        else:
            self.setWindowTitle(f"Threads: {threads_num}")

    def _update_states(self):
        self._update_window_title()

        row = self.table_thread.currentRow()
        ok = row != -1

        self.button_pause.setEnabled(ok and not self.get_thread(row).is_pause())
        self.button_resume.setEnabled(ok and self.get_thread(row).is_pause())

        if ok:
            title = self.table_thread.item(row, 0).text()
            self.button_pause.setText(f"Pause - {title!r}")
            self.button_resume.setText(f"Resume - {title!r}")

        threads_num = self.table_thread.rowCount()
        self.button_pause_all.setEnabled(threads_num)
        self.button_resume_all.setEnabled(threads_num)

    def get_thread(self, row: int) -> Thread:
        return self.table_thread.item(row, 0).data(Qt.UserRole)

    def get_all_thread(self) -> list[Thread]:
        return [self.get_thread(row) for row in range(self.table_thread.rowCount())]

    def update_info(self):
        self._update_window_title()

        if self.cb_reset_sum.isChecked():
            self._sum = 0

        self._sum += sum(thread.sum for thread in self.get_all_thread())
        self.label_result.setText(f"TOTAL SUM: <b>{get_pretty_int(self._sum)}</b>")

    def _on_thread_changed(self, thread: Thread):
        for row in range(self.table_thread.rowCount()):
            if thread == self.get_thread(row):
                self.table_thread.item(row, 1).setText(thread.get_state())
                self.table_thread.item(row, 2).setText(get_pretty_int(thread.sum))

    def add(self):
        if not self.started:
            self.started = dt.datetime.now()

        thread = Thread(self)
        thread.about_sum.connect(
            lambda _, thread=thread: self._on_thread_changed(thread)
        )
        thread.about_pause.connect(
            lambda _, thread=thread: self._on_thread_changed(thread)
        )

        row = self.table_thread.rowCount()
        self.table_thread.setRowCount(row + 1)

        title = f"Thread #{row + 1}"
        item_title = QTableWidgetItem(title)
        item_title.setData(Qt.UserRole, thread)

        item_state = QTableWidgetItem(thread.get_state())
        item_sum = QTableWidgetItem(str(thread.sum))

        self.table_thread.setItem(row, 0, item_title)
        self.table_thread.setItem(row, 1, item_state)
        self.table_thread.setItem(row, 2, item_sum)

        thread.start()

        self._update_states()

    def pause(self):
        item = self.table_thread.currentItem()
        if item:
            thread = self.get_thread(item.row())
            thread.pause()

        self._update_states()

    def pause_all(self):
        for thread in self.get_all_thread():
            thread.pause()

        self._update_states()

    def resume(self):
        item = self.table_thread.currentItem()
        if item:
            thread = self.get_thread(item.row())
            thread.resume()

        self._update_states()

    def resume_all(self):
        for thread in self.get_all_thread():
            thread.resume()

        self._update_states()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.resize(800, 300)
    mw.show()

    sys.exit(app.exec_())
