#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from urllib.request import urlopen
from urllib.parse import quote

from bs4 import BeautifulSoup


query = "сбер".encode("windows-1251")
url = "http://www.cbr.ru/scripts/XML_bic.asp?name=" + quote(query)
with urlopen(url) as f:
    root = BeautifulSoup(f.read(), "xml")

    for i, record in enumerate(root.find_all("Record"), 1):
        name = record.find("ShortName").text
        bic = record.find("Bic").text

        print('{}. "{}", {}, {}'.format(i, name, bic, record["DU"]))
