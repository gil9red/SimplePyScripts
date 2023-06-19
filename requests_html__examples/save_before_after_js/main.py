#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install requests-html
from requests_html import HTMLSession


session = HTMLSession()
rs = session.get("https://coronavirus-monitor.ru/statistika/")
with open("rs_before_js.html", "w", encoding="utf-8") as f:
    f.write(rs.html.html)

rs.html.render()  # Без этого не будет выполнения js кода

with open("rs_after_js.html", "w", encoding="utf-8") as f:
    f.write(rs.html.html)
