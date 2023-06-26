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


from PyQt5 import Qt

from FramelessWindow import FramelessWindow


class MainWindow(Qt.QWidget):
    def __init__(self, frameless_window):
        super().__init__()

        # Использовать шрифты Webdings для отображения значков
        font = self.font()
        font.setFamily('Webdings')

        self.buttonMy = Qt.QPushButton('@', clicked=self._on_process_clicked, font=font)
        self.buttonMy.setStyleSheet("""
* {
    border: none;
    background-color: rgb(54, 157, 180);
}
*:hover {
    color: white;
    background-color: green;   /* rgb(232, 17, 35) */
}
        """)

        self.line_edit_my = Qt.QLineEdit('Test!', returnPressed=self._on_process_clicked)

        # TODO: append setColor for Title / support transparent
        self.titleBar = frameless_window.titleBar
        self.titleBar.addWidget(self.line_edit_my, width=75, height=20)
        self.titleBar.addWidget(self.buttonMy)

        self.textEdit = Qt.QTextEdit()

        layout = Qt.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(Qt.QCommandLinkButton('Click!', clicked=lambda: self.textEdit.append('>>> ')))
        layout.addWidget(self.textEdit)

        self.setLayout(layout)

    def _on_process_clicked(self):
        self.textEdit.append(f"Нажата `Своя Кнопка` -> '{self.line_edit_my.text()}'!")


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    w = FramelessWindow()
    w.setWindowTitle('Тестовая строка заголовка')
    w.setWindowIcon(Qt.QIcon('icon.ico'))

    # Добавить свое окно
    w.setWidget(MainWindow(w))
    w.show()

    sys.exit(app.exec_())
