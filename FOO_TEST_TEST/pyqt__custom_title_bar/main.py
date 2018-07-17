#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Created on 2018年4月30日
# author: Irony
# site: https://github.com/892768447
# email: 892768447@qq.com
# file: Test
# description:
__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = 'Copyright (c) 2018 Irony'
__Version__ = 1.0


# SOURCE: https://github.com/892768447/PyQt/blob/f6ff3ee8bf8e7e9dd8d3ba3d39cf5cefa3c91e7b/%E6%97%A0%E8%BE%B9%E6%A1%86%E8%87%AA%E5%AE%9A%E4%B9%89%E6%A0%87%E9%A2%98%E6%A0%8F%E7%AA%97%E5%8F%A3/Test.py


from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit

from FramelessWindow import FramelessWindow


class MainWindow(QWidget):
    def __init__(self, frameless_window):
        super().__init__()

        self.titleBar = frameless_window.titleBar
        self.titleBar.signalButtonMy.connect(self.onButtonMy)

        self.textEdit = QTextEdit()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QPushButton('Кнопка'))
        layout.addWidget(self.textEdit)

        self.setLayout(layout)

    def onButtonMy(self):
        self.textEdit.append("Нажата `Своя Кнопка`!")


# стиль
STYLE_SHEET = """
/* Панель заголовка */
TitleBar {
    background-color: rgb(54, 157, 180);
}
/* Минимизировать кнопку `Максимальное выключение` Общий фон по умолчанию */
#buttonMinimum,#buttonMaximum,#buttonClose, #buttonMy {
    border: none;
    background-color: rgb(54, 157, 180);
}
/* Зависание */
#buttonMinimum:hover,#buttonMaximum:hover {
    background-color: rgb(48, 141, 162);
}
#buttonClose:hover {
    color: white;
    background-color: rgb(232, 17, 35);
}
#buttonMy:hover {
    color: white;
    background-color: green;   /* rgb(232, 17, 35) */
}
/* Мышь удерживать */
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: rgb(44, 125, 144);
}
#buttonClose:pressed {
    color: white;
    background-color: rgb(161, 73, 92);
}
"""


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    # TODO: FramelessWindow.setStyleSheet
    app.setStyleSheet(STYLE_SHEET)
    w = FramelessWindow()
    w.setWindowTitle('Тестовая строка заголовка')
    w.setWindowIcon(QIcon('Qt.ico'))
    w.setWidget(MainWindow(w))          # Добавить свое окно
    w.show()
    sys.exit(app.exec_())
