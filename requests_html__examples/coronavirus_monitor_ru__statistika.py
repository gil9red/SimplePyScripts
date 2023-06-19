#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install requests-html
from requests_html import HTMLSession


session = HTMLSession()
rs = session.get("https://coronavirus-monitor.ru/statistika/")
rs.html.render()  # Без этого не будет выполнения js кода

for row in rs.html.find("#statistics .total-table-row"):
    name = row.find(".name", first=True).text.rstrip(":")
    value = row.find(".value", first=True).text

    print(name, value)

# Зараженных 1635879
# Тяжелобольных 1097
# На подозрении 1141
# Смертей 99420
# Вылеченных 368052
