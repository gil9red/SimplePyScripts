#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from lxml import html
import requests


def get_text(node):
    return html.tostring(node, encoding='unicode', method='text', with_tail=False)


URL = 'https://m.vk.com/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'DNT': '1'
}

LOGIN = '<LOGIN>'
PASSWORD = '<PASSWORD>'


session = requests.session()
rs = session.get(URL, headers=HEADERS)
root = html.fromstring(rs.content)

form = root.forms[0]
form.fields['email'] = LOGIN
form.fields['pass'] = PASSWORD

rs = session.post(form.action, data=form.form_values())
root = html.fromstring(rs.content)

for li in root.cssselect('.main_menu > li'):
    print(get_text(li))
# Новости
# Уведомления
# Сообщения
# Друзья
# Группы
# Фотографии
# Закладки
# Поиск
