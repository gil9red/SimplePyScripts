#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


url = "http://www.dns-shop.ru/"

rs = requests.get(url)
root = BeautifulSoup(rs.content, "html.parser")

for item in root.select("#payment-variants > span"):
    print(item["title"])
