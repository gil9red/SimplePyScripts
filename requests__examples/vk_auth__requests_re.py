#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


def auth(
    login: str, password: str
) -> (requests.sessions.Session, requests.models.Response):
    """
    Функция для авторизации в вк.

    """

    def get_form_action(html: str) -> str:
        """
        Функция вернет ссылку для запроса авторизации

        """

        form_action = re.findall(r'<form(?= ).* action="(.+)"', html)
        if form_action:
            return form_action[0]

    session = requests.Session()

    # Без авторизации не получится воспользоваться страницей укорачивания ссылок
    url = "https://m.vk.com"
    rs = session.get(url)
    print(rs)

    login_form_action = get_form_action(rs.text)
    if not login_form_action:
        raise Exception(
            "Не получилось из формы авторизации вытащить ссылку на авторизацию"
        )

    login_form_data = {
        "email": login,
        "pass": password,
    }
    rs = session.post(login_form_action, login_form_data)
    print(rs, type(rs))

    return session, rs


if __name__ == "__main__":
    LOGIN = "<LOGIN>"
    PASSWORD = "<PASSWORD>"

    session, rs = auth(LOGIN, PASSWORD)
    print(session, session.cookies)
    print(rs, rs.url)
    print()

    from bs4 import BeautifulSoup

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
