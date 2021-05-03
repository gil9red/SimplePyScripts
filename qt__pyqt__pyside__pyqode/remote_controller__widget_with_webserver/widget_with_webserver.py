#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, jsonify

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit
from PyQt5.QtCore import QThread, pyqtSignal

from config import PORT


class CommandServerThread(QThread):
    about_command = pyqtSignal(str)

    def __init__(self, parent=None, port=20000):
        super().__init__(parent)

        self.port = port
        self.app = Flask(__name__)

        @self.app.route("/command/<command>", methods=['POST'])
        def command(command: str):
            print(command)
            self.about_command.emit(command)

            return jsonify({'status': True})

    def run(self):
        self.app.run(port=self.port)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('MainWindow + CommandServerThread')

        log_edit = QPlainTextEdit()

        layout = QVBoxLayout(self)
        layout.addWidget(log_edit)

        self.thread = CommandServerThread(self, port=PORT)
        self.thread.about_command.connect(log_edit.appendPlainText)
        self.thread.start()


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
