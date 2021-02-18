#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from typing import List, Tuple

import requests
from bs4 import BeautifulSoup


URL = 'https://www.sslproxies.org/'

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'


def get_proxies(by_code: str = None) -> List[Tuple[str, int, str]]:
    items = []

    rs = session.get(URL)
    root = BeautifulSoup(rs.content, 'html.parser')

    for tr in root.select('#proxylisttable > tbody > tr'):
        td_host, td_port, td_code = tr.select('td')[:3]
        host = td_host.get_text(strip=True)
        port = int(td_port.get_text(strip=True))
        code = td_code.get_text(strip=True)
        if by_code and by_code != code:
            continue

        items.append((host, port, code))

    return items


if __name__ == '__main__':
    items = get_proxies()
    print(len(items), items)
    # 100 [('191.100.20.14', 8080, 'EC'), ..., ('185.198.188.55', 8080, 'GB')]

    items_ru = get_proxies(by_code='RU')
    print(len(items_ru), items_ru)
    # 9 [('95.165.163.188', 60103, 'RU'), ..., ('94.141.117.1', 8080, 'RU')]

    print()

    # Test
    import random
    for host, port, _ in random.choices(items, k=5):
        proxies = {
            'http': f'http://{host}:{port}',
            'https': f'https://{host}:{port}',
        }
        try:
            rs = requests.get('https://api.ipify.org/', proxies=proxies, timeout=5)
            print(f'{host}:{port} -> {rs.text}')
        except:
            print(f'[#] {host}:{port} -> proxy error!')
    """
    [#] 104.218.240.70:999 -> proxy error!
    [#] 88.99.134.61:8080 -> proxy error!
    18.179.4.92:80 -> 18.179.4.92
    185.198.188.53:8080 -> 185.198.189.21
    [#] 109.170.97.146:8085 -> proxy error!
    """
