#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from lxml import html


def get_text(node):
    return html.tostring(node, encoding="unicode", method="text", with_tail=False)


LOGIN = "<LOGIN>"
PASSWORD = "<PASSWORD>"


session = requests.session()
rs = session.get("https://m.vk.com/")
root = html.fromstring(rs.content)

form = root.forms[0]
form.fields["email"] = LOGIN
form.fields["pass"] = PASSWORD

rs = session.post(form.action, data=form.form_values())
root = html.fromstring(rs.content)

for li in root.cssselect(".main_menu > li"):
    print(get_text(li))
# Новости
# Уведомления
# Сообщения
# Друзья
# Группы
# Фотографии
# Закладки
# Поиск
