#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from bs4 import BeautifulSoup
from hyper import HTTPConnection


conn = HTTPConnection("maxmaster.ru:443")
conn.request("GET", "/")
resp = conn.get_response()
print(resp.status)
# 200

root = BeautifulSoup(resp.read(), "html.parser")
print(root.select_one("head > title").text)
# MAXMASTER - интернет-магазин электроинструмента, ...
