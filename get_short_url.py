#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.request import urlopen


def get_short_url(url):
    """Функция возвращает короткую ссылку на url.
    Для этого она использует сервис clck.ru

    """

    with urlopen("https://clck.ru/--?url=" + url) as rs:
        return rs.read().decode()


if __name__ == "__main__":
    url = "https://www.google.ru/search?q=short+url+python"
    print(get_short_url(url))
