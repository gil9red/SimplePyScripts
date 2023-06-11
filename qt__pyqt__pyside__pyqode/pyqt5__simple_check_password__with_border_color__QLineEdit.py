#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Check password")

        self.le_target_password = QLineEdit("123")
        self.le_current_password = QLineEdit()
        self.le_current_password.textEdited.connect(self._on_check_password)

        self.label_result = QLabel()

        main_layout = QFormLayout()
        main_layout.addRow("Current password", self.le_target_password)
        main_layout.addRow("Password", self.le_current_password)
        main_layout.addWidget(self.label_result)

        self.setLayout(main_layout)

    def _on_check_password(self):
        text = '<font color="{}">{}</font>'

        if self.le_target_password.text() == self.le_current_password.text():
            text = text.format("darkgreen", "Пароль правильный!")
            self.le_current_password.setStyleSheet("border: 3px solid darkgreen;")

        else:
            text = text.format("red", "Пароль неправильный!")
            self.le_current_password.setStyleSheet("border: 3px solid red;")

        self.label_result.setText(text)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
