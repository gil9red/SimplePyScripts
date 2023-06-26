#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


data = open("example_rq.xml", "rb").read()
url = "http://smev-mvf.test.gosuslugi.ru:7777/gateway/services/SID0003663/wsdl"

rs = requests.post(url, data=data)
print(rs)

with open("example_rs.xml", "wb") as f:
    f.write(rs.content)

root = BeautifulSoup(rs.content, "html.parser")
print(root.prettify())
