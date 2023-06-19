#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
import requests


LOGIN = "<LOGIN>"
PASSWORD = "<PASSWORD>"


session = requests.session()
rs = session.get("https://m.vk.com/")
root = BeautifulSoup(rs.content, "html.parser")

form = root.select_one("form")
form_action = form["action"]

data = {"email": LOGIN, "pass": PASSWORD}

rs = session.post(form_action, data=data)
root = BeautifulSoup(rs.content, "html.parser")

for li in root.select(".main_menu > li"):
    print(li.text)
# Новости
# Уведомления
# Сообщения
# Друзья
# Группы
# Фотографии
# Закладки
# Поиск
