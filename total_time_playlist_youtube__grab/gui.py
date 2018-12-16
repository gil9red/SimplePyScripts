#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

try:
    from PyQt5.QtWidgets import *

except:
    try:
        from PyQt4.QtGui import *

    except:
        from PySide.QtGui import *

from total_time_playlist_youtube import count_total_playlist_time
import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('total_time_playlist_youtube')

        self.url_line_edit = QLineEdit()
        self.url_line_edit.returnPressed.connect(self.go)

        self.go_button = QPushButton('Go!')
        self.go_button.clicked.connect(self.go)

        self.result_label = QLabel()

        layout = QHBoxLayout()
        layout.addWidget(self.url_line_edit)
        layout.addWidget(self.go_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.result_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def go(self):
        try:
            url = self.url_line_edit.text()
            total_seconds = count_total_playlist_time(url, config.proxy, config.proxy_type)

            from datetime import timedelta
            text = 'Total time: {} ({} total seconds).'.format(timedelta(seconds=total_seconds), total_seconds)
            print('\n' + text)

            self.result_label.setText(text)

        except Exception as e:
            import traceback
            text = str(e) + '\n\n' + traceback.format_exc()

            self.result_label.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    # Пусть хоть что-то будет по умолчанию
    mw.url_line_edit.setText('https://www.youtube.com/playlist?list=PLvX4-HTvsLu-j-K9n14cV5OvxwBl_8Won')

    app.exec_()
