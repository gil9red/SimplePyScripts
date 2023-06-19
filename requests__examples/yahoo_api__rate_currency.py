#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# TODO: использовать http://www.cbr.ru/scripts/Root.asp?PrtId=SXML или разобраться с данными от query.yahooapis.com
# непонятны некоторые параметры
# TODO: сделать консоль
# TODO: сделать гуй
# TODO: сделать сервер
import requests


rs = requests.get(
    "https://query.yahooapis.com/v1/public/yql?q=select+*+from+yahoo.finance.xchange+where+pair+=+%22USDRUB,EURRUB%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
)
print(rs.json())

for rate in rs.json()["query"]["results"]["rate"]:
    print(rate["Name"], rate["Rate"])
