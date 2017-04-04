#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_short_link_from_vk(login: str, password: str, link: str) -> str:
    """
    Функция для получения короткой ссылки используя сервис vk.

    """

    def get_form_action(html: str) -> str:
        """
        Функция вернет ссылку для запроса авторизации

        """

        import re
        form_action = re.findall(r'<form(?= ).* action="(.+)"', html)
        if form_action:
            return form_action[0]

    import requests
    session = requests.Session()

    # Без авторизации не получится воспользоваться страницей укорачивания ссылок
    url = 'https://m.vk.com'
    rs = session.get(url)
    print(rs)

    login_form_action = get_form_action(rs.text)
    if not login_form_action:
        raise Exception('Не получилось из формы авторизации вытащить ссылку на авторизацию')

    login_form_data = {
        'email': login,
        'pass': password,
    }
    rs = session.post(login_form_action, login_form_data)
    print(rs)

    # Страница нужна чтобы получить hash для запроса
    rs = session.get('https://vk.com/cc')

    import re
    match = re.search(r"Shortener\.submitLink\('(.+)'\)", rs.text)
    if match is None:
        raise Exception('Не удалось получить hash для Shortener')

    shortener_hash = match.group(1)

    # Данные для POST запроса для получения короткой ссылки
    data = {
        'act': 'shorten',
        'link': link,
        'al': '1',
        'hash': shortener_hash,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    rs = session.post('https://vk.com/cc', headers=headers, data=data)
    print(rs)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    a_short_link = root.select_one('.shortened_link.shorten_list_header > a[href]')
    return a_short_link['href']


if __name__ == '__main__':
    LOGIN = '<LOGIN>'
    PASSWORD = '<PASSWORD>'
    link = 'https://ru.stackoverflow.com/questions/648230'

    short_link = get_short_link_from_vk(LOGIN, PASSWORD, link)
    print(short_link)  # https://vk.cc/6sYwPq

    link = 'https://git-scm.com/book/ru/v1/%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B-Git-%D0%9F%D1%80%D0%BE%D1%81%D0%BC%D0%BE%D1%82%D1%80-%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8-%D0%BA%D0%BE%D0%BC%D0%BC%D0%B8%D1%82%D0%BE%D0%B2'
    short_link = get_short_link_from_vk(LOGIN, PASSWORD, link)
    print(short_link)  # https://vk.cc/5AJUvX
