#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import Qt, QKeyEvent, QApplication, QPushButton, QTimer


def key_press_release(widget, key, modifier=Qt.NoModifier) -> None:
    """
    Функция для отправления события нажатия кнопки.
    # Имитация нажатия на пробел:
    key_press_release(widget, Qt.Key_Space)
    """

    key_press = QKeyEvent(QKeyEvent.KeyPress, key, modifier, None, False, 0)
    QApplication.sendEvent(widget, key_press)

    key_release = QKeyEvent(QKeyEvent.KeyRelease, key, modifier, None, False, 0)
    QApplication.sendEvent(widget, key_release)


if __name__ == "__main__":
    app = QApplication([])

    button = QPushButton("Click!")
    button.clicked.connect(lambda: print("Hello World!"))
    button.show()

    timer = QTimer()
    timer.timeout.connect(lambda: key_press_release(button, Qt.Key_Space))
    timer.setInterval(1000)
    timer.start()

    app.exec()
