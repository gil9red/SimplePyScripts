#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from robobrowser import RoboBrowser


LOGIN = "<LOGIN>"
PASSWORD = "<PASSWORD>"


browser = RoboBrowser(
    user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    parser="lxml",
)
browser.open("https://m.vk.com")

signup_form = browser.get_form()
signup_form["email"].value = LOGIN
signup_form["pass"].value = PASSWORD

# Submit the form
browser.submit_form(signup_form)

print(browser.url)

for li in browser.select(".main_menu > li"):
    print(li.text)
# Новости
# Уведомления
# Сообщения
# Друзья
# Группы
# Фотографии
# Закладки
# Поиск
