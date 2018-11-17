#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_short_link_from_vk(login: str, password: str, link: str) -> str:
    """
    Функция для получения короткой ссылки используя сервис vk.

    """

    from vk_auth__requests_re import auth
    session, rs = auth(login, password)

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
