#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob
import os
import sys
import time
import traceback

from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *

except:
    try:
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *

    except:
        from PySide.QtGui import *
        from PySide.QtCore import *

from main import sizeof_fmt


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


# Нужен отдельный поток, чтобы при выполнении кода в нем гуяшный поток не тормозил
class SearchThread(QThread):
    about_new_text = pyqtSignal(str)

    def run(self):
        # "-u : unbuffered binary stdout and stderr." Иначе, при запуске питона, пока н завершится скрипт
        # данные с stdout и stderr не будут получены
        command = [sys.executable, "-u", "main.py"]

        self.about_new_text.emit(f'Execute: "{" ".join(command)}"')

        rs = Popen(command, universal_newlines=True, stdout=PIPE, stderr=STDOUT)
        for line in rs.stdout:
            line = line.rstrip()
            self.about_new_text.emit(line)


class EmptyFoldersTab(QWidget):
    about_new_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.line_list = None

        self.line_edit_filter = QLineEdit()
        self.line_edit_filter.setToolTip("Filter")
        self.line_edit_filter.textEdited.connect(self._reread_list)

        self.push_button_show_in_explorer = QPushButton("Show in explorer")
        self.push_button_show_in_explorer.clicked.connect(self._on_show_in_explorer)

        self.push_button_remove_folder = QPushButton("Remove folder")
        self.push_button_remove_folder.clicked.connect(self._on_remove_folder)

        self.model = QStringListModel()

        self.view = QListView()
        self.view.setEditTriggers(QListView.NoEditTriggers)
        self.view.setAlternatingRowColors(True)
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self._on_show_in_explorer)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.push_button_show_in_explorer)
        layout_buttons.addWidget(self.push_button_remove_folder)

        layout_filter = QHBoxLayout()
        layout_filter.addWidget(QLabel("Search:"))
        layout_filter.addWidget(self.line_edit_filter)

        layout = QVBoxLayout()
        layout.addLayout(layout_buttons)
        layout.addLayout(layout_filter)
        layout.addWidget(self.view)
        self.setLayout(layout)

    def _on_show_in_explorer(self, index=None):
        if not index:
            index = self.view.currentIndex()
            if index is None:
                return

        file_name = self.model.data(index, Qt.DisplayRole)

        cmd = f'Explorer /n,"{file_name}"'
        self.about_new_text.emit(f"Run command: {cmd}")

        os.system(cmd)

    def _on_remove_folder(self):
        index = self.view.currentIndex()
        if index is None:
            return

        file_name = self.model.data(index, Qt.DisplayRole)

        if not os.path.exists(file_name):
            QMessageBox.information(
                self, "Info", f'File "{file_name}" not exists!'
            )

        msg_box = QMessageBox(
            QMessageBox.Question, "Question", f'Remove file: "{file_name}"?'
        )
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        result = msg_box.exec()
        if result != QMessageBox.Ok:
            return

        self.about_new_text.emit(f'Remove file: "{file_name}"')

        try:
            os.rmdir(file_name)
            self.model.removeRow(index.row())

        except PermissionError as e:
            QMessageBox.critical(None, "PermissionError", str(e))

    def _reread_list(self):
        if not self.line_list:
            return

        new_line_list = self.line_list

        filter_text = self.line_edit_filter.text()
        if filter_text:
            filter_text = filter_text.lower()
            new_line_list = [
                line for line in self.line_list if filter_text in line.lower()
            ]

        self.model.setStringList(new_line_list)

        if new_line_list:
            self.view.setCurrentIndex(self.model.index(0))

    def fill(self, file_name):
        self.about_new_text.emit("Start fill: " + file_name)

        t = time.clock()

        with open(file_name, mode="rb") as f:
            byte_data = f.read()
            data = byte_data.decode("utf-8")

        self.about_new_text.emit(
            f'  Size of "{file_name}": {sizeof_fmt(len(byte_data))}'
        )

        self.line_list = data.splitlines()
        self.about_new_text.emit(f"  Lines: {len(self.line_list)}")

        self._reread_list()

        self.about_new_text.emit(
            f"Finish fill, elapsed time: {time.clock() - t:.3f} secs"
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"search_of_empty_folders [{sys.executable}]")

        self.text_edit_log = QTextEdit()

        self.push_button_start = QPushButton("Start")
        self.push_button_start.clicked.connect(self._start_search)

        self.push_button_clear_log = QPushButton("Clear log")
        self.push_button_clear_log.clicked.connect(self.text_edit_log.clear)

        layout_main_page = QVBoxLayout()
        layout_main_page_buttons = QHBoxLayout()
        layout_main_page_buttons.addWidget(self.push_button_start)
        layout_main_page_buttons.addWidget(self.push_button_clear_log)

        layout_main_page.addLayout(layout_main_page_buttons)
        layout_main_page.addWidget(self.text_edit_log)

        self.main_page = QWidget()
        self.main_page.setLayout(layout_main_page)

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.main_page, "Main page")

        self.setCentralWidget(self.tab_widget)

    def append_log(self, text):
        time_str = datetime.today().strftime("%H:%M:%S")
        self.text_edit_log.append(time_str + ": " + text)

    def _start_search(self):
        t = time.clock()

        self.append_log("Start search")

        # Удаление всех вкладок, кроме главной
        for i in reversed(range(1, self.tab_widget.count())):
            self.tab_widget.removeTab(i)

        self.push_button_start.setEnabled(False)

        self.append_log("")
        self.append_log("  Start thread")

        thread = SearchThread()
        # Отслеживание сообщений от потока и при добавлении в лог дополнительный отступ
        thread.about_new_text.connect(lambda text: self.append_log("    " + text))
        thread.start()

        # QEventLoop нужен чтобы при запуске потока выполнение кода главного
        # потока остановилось здесь и продолжилось только после завершения потока
        loop = QEventLoop()
        thread.finished.connect(loop.quit)
        loop.exec()

        self.append_log("  Finish thread")

        self.append_log("")

        file_name_list = glob.glob("log of*.txt")
        self.append_log(f"  Found logs: {', '.join(file_name_list)}")

        self.append_log("")
        self.append_log("  Create tabs")

        empty_folders_tab_list = []

        for file_name in file_name_list:
            tab = EmptyFoldersTab()
            # Отслеживание сообщений от вкладки и при добавлении в лог дополнительный отступ
            tab.about_new_text.connect(lambda text: self.append_log("    " + text))

            empty_folders_tab_list.append((tab, file_name))
            self.tab_widget.addTab(tab, file_name)

            self.append_log(f'    Create tab "{file_name}"')

        self.append_log("  Finish create tabs")

        self.append_log("")
        self.append_log("  Fill tabs")

        for i, (tab, file_name) in enumerate(empty_folders_tab_list, 1):
            tab.fill(file_name)

            # Заморочка, чтобы для последнего элемента не печатался пустой лог
            if i != len(empty_folders_tab_list):
                self.append_log("")

        self.append_log("  Finish fill tabs")
        self.append_log("")

        self.push_button_start.setEnabled(True)

        self.append_log(
            f"Finish search, elapsed time: {time.clock() - t:.3f} secs"
        )


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()
    mw.resize(800, 600)

    sys.exit(app.exec_())
