#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from typing import Optional

import requests


session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'


def get_price(url: str) -> Optional[int]:
    rs = session.get(url)

    m = re.search(r'"price":(\d+)', rs.text)
    if not m:
        print('[#] price not found from regex!')
        return

    price = int(m.group(1))

    # При отсутствии цены, значением у нее будет 0
    if price == 0:
        return

    return price


if __name__ == '__main__':
    for url in [
        'https://www.dns-shop.ru/product/4d664a0d90d61b80/processor-amd-ryzen-7-3700x-oem/',
        'https://technopoint.ru/product/4d664a0d90d61b80/processor-amd-ryzen-7-3700x-oem-sale/',
        'https://www.dns-shop.ru/product/8385e84a50f73332/operativnaa-pamat-neo-forza-encke-nmud416e82-3200dc20-32-gb/',
        'https://technopoint.ru/product/8385e84a50f73332/operativnaa-pamat-neo-forza-encke-nmud416e82-3200dc20-32-gb-sale/',
    ]:
        price = get_price(url)
        print(f'Price: {price}, url: {url}')

    # Price: 23299, url: https://www.dns-shop.ru/product/4d664a0d90d61b80/processor-amd-ryzen-7-3700x-oem/
    # Price: 22899, url: https://technopoint.ru/product/4d664a0d90d61b80/processor-amd-ryzen-7-3700x-oem-sale/
    # Price: 11299, url: https://www.dns-shop.ru/product/8385e84a50f73332/operativnaa-pamat-neo-forza-encke-nmud416e82-3200dc20-32-gb/
    # Price: 11099, url: https://technopoint.ru/product/8385e84a50f73332/operativnaa-pamat-neo-forza-encke-nmud416e82-3200dc20-32-gb-sale/
