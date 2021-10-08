#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'


url = 'https://winauto.ua/index.php?match=all&subcats=y&pcode_from_q=y&pshort=y&pfull=y&pname=y&pkeywords=y&search_performed=y&q=gazer&dispatch=products.search&items_per_page=128&search_id=37901&page=1'
rs = session.get(url)
root = BeautifulSoup(rs.content, 'html.parser')

for product in root.select('#products_search_pagination_contents .ut2-gl__body'):
    title = product.select_one('.product-title').get_text(strip=True)
    price = product.select_one('.ty-price-update img[title]')
    if not price:
        print(f'[#] Не удалось найти цену для {title!r}!')
        continue

    print(title, price['title'], sep=" | ")

"""
Видеорегистратор Gazer F155 c GPS, Wi-Fi, LTE с охранным режимом | Цена: 5999 грн.
Видеорегистратор Gazer F750w | Цена: 9999 грн.
Блок для подключения к CAN-шине Gazer MA011 для Volkswagen, Skoda, Seat | Цена: 970 грн.
...
Штатная магнитола Gazer CM6006-SC11 для Nissan Tiida(SC11), Qashqai, X-Trail, Patrol 2004-2010 | Цена: 15992 грн.
Штатная магнитола Gazer CM5008-XW50 для Toyota Prius (XW50) 2014-2017 | Цена: 7109 грн.
Штатная магнитола Gazer CM6509-QL для Kia Sportage (QL) 2015-2017 | Цена: 21990 грн.
"""