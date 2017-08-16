#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: добавить строку с фильтром

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


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


import time


# Нужен отдельный поток, чтобы при выполнении кода в нем гуяшный поток не тормозил
class SearchThread(QThread):
    about_new_text = pyqtSignal(str)

    def run(self):
        import sys
        command = sys.executable + ' main.py'

        self.about_new_text.emit('Execute: "{}"'.format(command))

        from subprocess import Popen, PIPE, STDOUT
        rs = Popen(command, universal_newlines=True, stdout=PIPE, stderr=STDOUT)
        for line in rs.stdout:
            line = line.rstrip()
            self.about_new_text.emit(line)


from main import sizeof_fmt


class EmptyFoldersTab(QWidget):
    about_new_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.push_button_show_in_explorer = QPushButton('Show in explorer')
        self.push_button_show_in_explorer.clicked.connect(self._on_show_in_explorer)

        self.push_button_remove_folder = QPushButton('Remove folder')
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

        layout = QVBoxLayout()
        layout.addLayout(layout_buttons)
        layout.addWidget(self.view)
        self.setLayout(layout)

    def _on_show_in_explorer(self, index=None):
        if not index:
            index = self.view.currentIndex()
            if index is None:
                return

        file_name = self.model.data(index, Qt.DisplayRole)

        cmd = 'Explorer /n,"{}"'.format(file_name)
        self.about_new_text.emit('Run command: {}'.format(cmd))

        import os
        os.system(cmd)

    def _on_remove_folder(self):
        index = self.view.currentIndex()
        if index is None:
            return

        file_name = self.model.data(index, Qt.DisplayRole)

        import os
        if not os.path.exists(file_name):
            QMessageBox.information(self, 'Info', 'File "{}" not exists!'.format(file_name))

        msg_box = QMessageBox(QMessageBox.Question, 'Question', 'Remove file: "{}"?'.format(file_name))
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        result = msg_box.exec()
        if result != QMessageBox.Ok:
            return

        self.about_new_text.emit('Remove file: "{}"'.format(file_name))

        try:
            os.rmdir(file_name)
            self.model.removeRow(index.row())

        except PermissionError as e:
            QMessageBox.critical(None, 'PermissionError', str(e))

    def fill(self, file_name):
        self.about_new_text.emit('Start fill: ' + file_name)

        t = time.clock()

        with open(file_name, mode='rb') as f:
            byte_data = f.read()
            data = byte_data.decode('utf-8')

        self.about_new_text.emit('Size of "{}": {}'.format(file_name, sizeof_fmt(len(byte_data))))

        line_list = data.splitlines()
        self.about_new_text.emit('Lines: {}'.format(len(line_list)))

        self.model.setStringList(line_list)
        if line_list:
            self.view.setCurrentIndex(self.model.index(0))

        self.about_new_text.emit('Finish fill, elapsed time: {:.3f} secs'.format(time.clock() - t))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('search_of_empty_folders')

        self.text_edit_log = QTextEdit()

        self.push_button_start = QPushButton('Start')
        self.push_button_start.clicked.connect(self._start_search)

        self.push_button_clear_log = QPushButton('Clear log')
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
        self.tab_widget.addTab(self.main_page, 'Main page')

        self.setCentralWidget(self.tab_widget)
    
    def append_log(self, text):
        from datetime import datetime
        time_str = datetime.today().strftime('%H:%M:%S')

        self.text_edit_log.append(time_str + ": " + text)
    
    def _start_search(self):
        t = time.clock()

        self.append_log('Start search')

        self.push_button_start.setEnabled(False)

        thread = SearchThread()
        thread.about_new_text.connect(self.append_log)
        thread.start()

        # QEventLoop нужен чтобы при запуске потока выполнение кода главного
        # потока остановилось здесь и продолжилось только после завершения потока
        loop = QEventLoop()
        thread.finished.connect(loop.quit)
        loop.exec()

        self.append_log('')

        import glob
        file_name_list = glob.glob('log of*.txt')
        self.append_log('Found logs: {}'.format(', '.join(file_name_list)))

        self.append_log('')
        self.append_log('Create tabs')

        empty_folders_tab_list = []

        for file_name in file_name_list:
            tab = EmptyFoldersTab()
            tab.about_new_text.connect(self.append_log)

            empty_folders_tab_list.append((tab, file_name))
            self.tab_widget.addTab(tab, file_name)

        self.append_log('Finish create tabs')

        self.append_log('')
        self.append_log('Fill tabs')

        for tab, file_name in empty_folders_tab_list:
            tab.fill(file_name)
            self.append_log('')

        self.append_log('Finish fill tabs')

        self.push_button_start.setEnabled(True)

        self.append_log('Finish search, elapsed time: {:.3f} secs'.format(time.clock() - t))


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()
    mw.resize(800, 600)

    sys.exit(app.exec_())
