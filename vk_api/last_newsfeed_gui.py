#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import vk_api
from PySide.QtGui import *


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.line_edit_login = QLineEdit()
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setEchoMode(QLineEdit.Password)

        self.spibox_count_newsfeed = QSpinBox()
        self.spibox_count_newsfeed.setValue(15)

        self.button_get_newsfeeds = QPushButton('Get newsfeeds')
        self.button_get_newsfeeds.clicked.connect(self.get_newsfeed)

        self.newsfeed = QTextEdit()

        layout = QFormLayout()
        layout.addRow("Login:", self.line_edit_login)
        layout.addRow("Password:", self.line_edit_password)
        layout.addRow("Count Newsfeed:", self.spibox_count_newsfeed)
        layout.addRow(self.button_get_newsfeeds)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.newsfeed)

        self.setLayout(main_layout)

    def get_newsfeed(self):
        try:
            vk = vk_api.VkApi(self.line_edit_login.text(), self.line_edit_password.text())
            vk.authorization()  # Авторизируемся

            text = ''

            newsfeed = vk.method('newsfeed.get', values={
                'filters': 'post',
                'count': self.spibox_count_newsfeed.value()
            })
            for i, feed in enumerate(newsfeed['items'], 1):
                text += '{}. {source_id} {date}: {text}\n'.format(i, **feed)

            self.newsfeed.setText(text)

        except Exception as e:
            QMessageBox.warning(None, None, str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    sys.exit(app.exec_())
