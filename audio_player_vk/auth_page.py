#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QMessageBox

import vk_api

from common import log


class AuthPage(QWidget):
    """Виджет предоставляет собой страницу авторизации."""

    about_successful_auth = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Объект для работы с vk api
        self.vk = None

        self.login = QLineEdit()
        self.login.returnPressed.connect(self.send_auth)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.send_auth)

        self.ok_button = QPushButton('Ok')
        self.ok_button.clicked.connect(self.send_auth)

        form_layout = QFormLayout()
        form_layout.addRow('Login:', self.login)
        form_layout.addRow('Password:', self.password)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.ok_button)
        layout.addStretch()

        self.setLayout(layout)

    def send_auth(self):
        log.debug('send_auth')

        login, password = self.login.text(), self.password.text()
        if not login or not password:
            QMessageBox.warning(self, 'Warning', 'Login or password is empty!')
            return

        # Пытаемся авторизоваться
        try:
            self.vk = vk_api.VkApi(login, password)
            self.vk.authorization()

        except Exception as e:
            QMessageBox.warning(self, 'Warning', 'Fail to authorize:\n' + str(e))
            return

        self.about_successful_auth.emit()
