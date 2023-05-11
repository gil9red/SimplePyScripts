#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Парсер курса доллара и евро за текущую дату от сайта центробанка России."""


import sys
from datetime import date

# pip install robobrowser
from robobrowser import RoboBrowser


date_req = date.today().strftime("%d.%m.%Y")
url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date_req

browser = RoboBrowser(
    user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    parser="html.parser",
)
browser.open(url)
rs = browser.response

if not rs.ok:
    print(rs.status_code, rs.reason)
    sys.exit()

for valute_el in browser.select("Valute"):
    char_code = valute_el.select_one("CharCode").get_text(strip=True)
    value = valute_el.select_one("Value").get_text(strip=True)

    if char_code in ["USD", "EUR"]:
        print(char_code, value)
