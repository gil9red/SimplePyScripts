#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PySide.QtGui import QApplication
from PySide.QtCore import QEventLoop
from PySide.QtWebKit import QWebSettings, QWebView
from PySide.QtNetwork import QNetworkProxyFactory


# Чтобы не было проблем запуска компов с прокси:
QNetworkProxyFactory.setUseSystemConfiguration(True)

QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

# Телефон или емейл
LOGIN = "<phone_or_email>"
PASSWORD = "<password>"

URL = "https://vk.com"


app = QApplication(sys.argv)

view = QWebView()
view.show()

view.load(URL)

loop = QEventLoop()
view.loadFinished.connect(loop.quit)
loop.exec_()

doc = view.page().mainFrame().documentElement()

email = doc.findFirst("#quick_email")
password = doc.findFirst("#quick_pass")
login_button = doc.findFirst("#quick_login_button")

if email.isNull() or password.isNull() or login_button.isNull():
    raise Exception(
        'Ошибка при авторизации: не найдены поля емейла или пароля, или кнопка "Войти".'
    )

# Заполняем поля емейла/телефона и пароля
email.setAttribute("value", LOGIN)
password.setAttribute("value", PASSWORD)

# Кликаем на кнопку "Войти"
login_button.evaluateJavaScript("this.click()")

sys.exit(app.exec_())
