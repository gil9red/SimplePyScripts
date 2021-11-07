#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import Union
import requests


session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'


def is_exists(app_id: Union[int, str]) -> bool:
    app_id = str(app_id)

    url = f'https://store.steampowered.com/app/{app_id}/'
    rs = session.get(url)
    return app_id in rs.url


if __name__ == '__main__':
    # Half-Life 2: Remastered Collection
    print(is_exists(600680))

    assert not is_exists(1)

    # DARK SOULS™: Prepare To Die Edition
    assert is_exists(211420)

    # Dota 2
    assert is_exists(570)
    assert is_exists('570')
