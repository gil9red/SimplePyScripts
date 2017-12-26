#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import *


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.login = QLineEdit()
        self.login.setPlaceholderText('Введите логин...')

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText('Введите пароль...')

        layout = QFormLayout()
        layout.addRow('Login:', self.login)
        layout.addRow('Password:', self.password)

        self.setLayout(layout)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Example')
        self.setCentralWidget(QLabel('<font size="100">Hello, <b>USER</b>!</font>'))


if __name__ == '__main__':
    app = QApplication([])

    password, ok = QInputDialog.getText(None, 'Auth', 'Input password:', QLineEdit.Password)
    if not ok:
        QMessageBox.warning(None, 'Warning', 'Need input password!')
        quit()

    if password != '123':
        QMessageBox.warning(None, 'Warning', 'Invalid password!')
        quit()

    w = Example()
    w.show()

    app.exec_()
