#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PySide.QtGui import QApplication, QKeyEvent
from PySide.QtCore import Qt


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
    import random
    import sys

    from PySide.QtCore import QEventLoop, QTimer
    from PySide.QtNetwork import QNetworkProxyFactory
    from PySide.QtWebKit import QWebView, QWebSettings

    app = QApplication(sys.argv)

    # Чтобы не было проблем запуска компов с прокси:
    QNetworkProxyFactory.setUseSystemConfiguration(True)

    QWebSettings.globalSettings().setAttribute(
        QWebSettings.DeveloperExtrasEnabled, True
    )

    view = QWebView()
    view.resize(400, 600)
    view.show()

    url = "http://gabrielecirulli.github.io/2048/"
    view.setWindowTitle(url)

    # Загрузка url и ожидание ее
    view.load(url)
    loop = QEventLoop()
    view.loadFinished.connect(loop.quit)
    loop.exec_()

    def random_click() -> None:
        """Функция для случайного клика на WASD."""

        key = random.choice([Qt.Key_W, Qt.Key_S, Qt.Key_A, Qt.Key_D])
        key_press_release(view, key)

    # Таймер для случайных кликов
    timer = QTimer()
    timer.timeout.connect(random_click)
    timer.start(333)

    app.exec_()

