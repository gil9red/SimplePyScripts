#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт оконной программы, которая показывает контрольную сумму файлов, кинутых на нее через drag-and-drop.

"""


import traceback

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QWidget, QFormLayout, QVBoxLayout
    from PyQt5.QtCore import Qt

except:
    from PyQt4.QtGui import QApplication, QMainWindow, QLabel, QMessageBox, QWidget, QFormLayout, QVBoxLayout
    from PyQt4.QtCore import Qt


from get_md5_file import md5sum


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    from datetime import datetime
    ts = datetime.today().timestamp()
    with open('error_text_{}'.format(ts), 'w', encoding='utf-8') as f:
        f.write(text)

    QMessageBox.critical(None, 'Error', text)
    quit()


import sys
sys.excepthook = log_uncaught_exceptions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('get_md5_file_gui')
        self.setAcceptDrops(True)

        self.label_file_name = QLabel()
        self.label_file_name.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_file_name.setWordWrap(True)

        self.label_md5 = QLabel()
        self.label_md5.setTextInteractionFlags(Qt.TextSelectableByMouse)

        layout = QFormLayout()
        layout.addRow('File name:', self.label_file_name)
        layout.addRow('MD5:', self.label_md5)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Drag and drop the file:'))
        main_layout.addLayout(layout)
        main_layout.addStretch()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if mime.hasUrls() and len(mime.urls()) == 1:
            event.acceptProposedAction()

    def dropEvent(self, event):
        url = event.mimeData().urls()[0]
        file_name = url.toLocalFile()
        md5_hex = md5sum(file_name)

        self.label_file_name.setText(file_name)
        self.label_md5.setText(md5_hex)

        return super().dropEvent(event)


if __name__ == '__main__':
    app = QApplication([])

    w = MainWindow()
    w.show()

    app.exec()
