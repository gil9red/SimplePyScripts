#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import *


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Animation check password")

        self.le_target_password = QLineEdit("123")

        self.le_current_password = QLineEdit()
        self.le_current_password.textEdited.connect(self._on_check_password)

        self.label_result = QLabel()

        main_layout = QFormLayout()
        main_layout.addRow("Current password", self.le_target_password)
        main_layout.addRow("Password", self.le_current_password)
        main_layout.addWidget(self.label_result)

        self.setLayout(main_layout)

        self.animation = QPropertyAnimation(self, b"password_border_color")
        self.animation.setDuration(1000)  # Продолжительность 1 секунда
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)

    def set_border_color_password(self, value) -> None:
        color = "0, 100, 0" if self.is_correct_password() else "255, 0, 0"
        self.le_current_password.setStyleSheet(
            f"border: 3px solid rgba({color}, {value});"
        )

    password_border_color = pyqtProperty(float, None, set_border_color_password)

    def is_correct_password(self):
        return self.le_target_password.text() == self.le_current_password.text()

    def _on_check_password(self) -> None:
        text = '<font color="{}">{}</font>'

        if self.is_correct_password():
            text = text.format("darkgreen", "Пароль правильный!")
        else:
            text = text.format("red", "Пароль неправильный!")

        self.animation.start()

        self.label_result.setText(text)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
