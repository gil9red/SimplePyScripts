#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication


def authorize(token) -> None:
    print(f"token: {token}")


def url_changed(url) -> None:
    url = url.toString()
    print(f"url_changed: {url}")

    match = re.search("access_token=([a-fA-F0-9]+)&?", url)
    if match:
        access_token = match.group(1)
        authorize(access_token)

    else:
        print(url, "doesn't match")


app_id = 5356487  # mini_vk_bot (никаких требований не запрашивает)
app_id = 3088991  # Игра "Проклятье часовщика" (хочет "Доступ к общей информации")

params = {
    "client_id": str(app_id),
    "display": "page",
    "redirect_uri": "https://oauth.vk.com/blank.html",
    "response_type": "token",
    # 'scope': 'messages',
    "v": "5.80",
}
link = "https://oauth.vk.com/authorize?" + "&".join(
    f"{k}={v}" for k, v in params.items()
)
# link = 'https://vk.com/'

app = QApplication([])

web = QWebEngineView()
web.load(QUrl(link))
web.urlChanged.connect(url_changed)
web.show()

app.exec()
