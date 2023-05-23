#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_products(search: str) -> list:
    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
    }
    url = f"https://www.dns-shop.ru/search/?q={search}&p=1&order=popular&stock=all"
    session = requests.session()
    session.headers.update(headers)

    rs = session.get(url)
    data = json.loads(rs.text)

    root = BeautifulSoup(data["html"], "html.parser")

    items = []

    for a in root.select(".product-info__title-link > a"):
        items.append(
            (a.get_text(strip=True), urljoin(rs.url, a["href"]))
        )

    return items


if __name__ == "__main__":
    name = "Видеокарты"
    items = get_products(name)

    print(f"Search {name!r}...")
    print(f"  Result ({len(items)}):")
    for title, url in items:
        print(f"    {title!r}: {url}")
    print()

    # Search 'Видеокарты'...
    #   Result (18):
    #     'Видеокарта MSI AMD Radeon RX 570 ARMOR OC [RX 570 ARMOR 8G OC]': https://www.dns-shop.ru/product/2bec09e3fc2e3330/videokarta-msi-amd-radeon-rx-570-armor-oc-rx-570-armor-8g-oc/
    #     'Видеокарта MSI GeForce RTX 2060 Super VENTUS OC [RTX 2060 SUPER VENTUS OC]': https://www.dns-shop.ru/product/06580877a9c61b80/videokarta-msi-geforce-rtx-2060-super-ventus-oc-rtx-2060-super-ventus-oc/
    #     'Видеокарта MSI GeForce RTX 2070 Super GAMING X TRIO [RTX 2070 SUPER GAMING X TRIO]': https://www.dns-shop.ru/product/893d7d1698bb3332/videokarta-msi-geforce-rtx-2070-super-gaming-x-trio-rtx-2070-super-gaming-x-trio/
    #     'Видеокарта Palit GeForce RTX 2060 Gaming Pro [NE62060018J9-1062A]': https://www.dns-shop.ru/product/89eb26e2156d1b80/videokarta-palit-geforce-rtx-2060-gaming-pro-ne62060018j9-1062a/
    #     'Видеокарта Sapphire AMD Radeon RX 590 PULSE [11289-06-20G]': https://www.dns-shop.ru/product/d4aa3e2690ab1b80/videokarta-sapphire-amd-radeon-rx-590-pulse-11289-06-20g/
    #     'Видеокарта Palit GeForce GTX 1660 DUAL OC [NE51660S18J9-1161A]': https://www.dns-shop.ru/product/25db5664658c3332/videokarta-palit-geforce-gtx-1660-dual-oc-ne51660s18j9-1161a/
    #     'Видеокарта GIGABYTE GeForce GTX 1660 OC [GV-N1660OC-6GD]': https://www.dns-shop.ru/product/38d7d1eb43d73332/videokarta-gigabyte-geforce-gtx-1660-oc-gv-n1660oc-6gd/
    #     'Видеокарта MSI AMD Radeon RX 570 ARMOR OC [RX 570 ARMOR 4G OC]': https://www.dns-shop.ru/product/90db0b7a1f5f3330/videokarta-msi-amd-radeon-rx-570-armor-oc-rx-570-armor-4g-oc/
    #     'Видеокарта GIGABYTE AMD Radeon RX 5700 XT GAMING OC [GV-R57XTGAMING OC-8GD]': https://www.dns-shop.ru/product/ec8f0a1dbfde1b80/videokarta-gigabyte-amd-radeon-rx-5700-xt-gaming-oc-gv-r57xtgaming-oc-8gd/
    #     'Видеокарта GIGABYTE GeForce RTX 2060 Super GAMING OC [GV-N206SGAMING OC-8GC]': https://www.dns-shop.ru/product/bfa21bf998943332/videokarta-gigabyte-geforce-rtx-2060-super-gaming-oc-gv-n206sgaming-oc-8gc/
    #     'Видеокарта MSI GeForce GTX 1660 VENTUS XS 6G OCV1 [GTX 1660 VENTUS XS 6G OCV1]': https://www.dns-shop.ru/product/1ef66abccb1e3332/videokarta-msi-geforce-gtx-1660-ventus-xs-6g-ocv1-gtx-1660-ventus-xs-6g-ocv1/
    #     'Видеокарта MSI GeForce GTX 1660 VENTUS XS OC [GTX 1660 VENTUS XS 6G OC]': https://www.dns-shop.ru/product/849575aa4ac13332/videokarta-msi-geforce-gtx-1660-ventus-xs-oc-gtx-1660-ventus-xs-6g-oc/
    #     'Видеокарта KFA2 GeForce RTX 2070 Super EX - 1 Click OC [27ISL6MDU9EK]': https://www.dns-shop.ru/product/ea111905a77a1b80/videokarta-kfa2-geforce-rtx-2070-super-ex---1-click-oc-27isl6mdu9ek/
    #     'Видеокарта MSI GeForce GTX 1660 Ti GAMING X [GTX 1660 TI GAMING X 6G]': https://www.dns-shop.ru/product/b3643ee130d03332/videokarta-msi-geforce-gtx-1660-ti-gaming-x-gtx-1660-ti-gaming-x-6g/
    #     'Видеокарта Sapphire AMD Radeon RX 570 PULSE [11266-66-20G]': https://www.dns-shop.ru/product/5a1c9bea39693332/videokarta-sapphire-amd-radeon-rx-570-pulse-11266-66-20g/
    #     'Видеокарта MSI GeForce RTX 2060 Super GAMING X [RTX 2060 SUPER GAMING X]': https://www.dns-shop.ru/product/12eaefb3a9c71b80/videokarta-msi-geforce-rtx-2060-super-gaming-x-rtx-2060-super-gaming-x/
    #     'Видеокарта MSI GeForce GTX 1660 Ti ARMOR OC [GTX 1660 Ti ARMOR 6G OC]': https://www.dns-shop.ru/product/c1bedbe329171b80/videokarta-msi-geforce-gtx-1660-ti-armor-oc-gtx-1660-ti-armor-6g-oc/
    #     'Видеокарта Sapphire AMD Radeon RX 590 NITRO+ Special Edition OC [11289-01-20G]': https://www.dns-shop.ru/product/9013d2b9e6da1b80/videokarta-sapphire-amd-radeon-rx-590-nitro-special-edition-oc-11289-01-20g/
