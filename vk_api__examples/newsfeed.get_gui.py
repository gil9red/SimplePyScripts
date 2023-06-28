#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QTextEdit,
    QFormLayout,
    QVBoxLayout,
    QMessageBox,
)

from root_common import vk_auth, LOGIN, PASSWORD


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.line_edit_login = QLineEdit(LOGIN)
        self.line_edit_password = QLineEdit(PASSWORD)
        self.line_edit_password.setEchoMode(QLineEdit.Password)

        self.spibox_count_newsfeed = QSpinBox()
        self.spibox_count_newsfeed.setValue(15)

        self.button_get_newsfeeds = QPushButton("Get newsfeeds")
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
            vk_session = vk_auth(
                self.line_edit_login.text(), self.line_edit_password.text()
            )
            newsfeed = vk_session.method(
                "newsfeed.get",
                values={"filters": "post", "count": self.spibox_count_newsfeed.value()},
            )

            items = []
            for i, feed in enumerate(newsfeed["items"], 1):
                items.append(f"{i}. {feed['source_id']} {feed['date']}: {feed['text']}")

            self.newsfeed.setText("\n".join(items))

        except Exception as e:
            print("Error:", traceback.format_exc())
            QMessageBox.warning(self, None, str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    sys.exit(app.exec_())
