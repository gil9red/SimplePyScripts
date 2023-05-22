#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


rs = requests.get("https://horo.mail.ru/prediction/pisces/today/")
root = BeautifulSoup(rs.content, "lxml")
text = root.select_one(".article__text").text.strip()
print(repr(text))
print(text)
