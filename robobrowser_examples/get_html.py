#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from robobrowser import RoboBrowser


browser = RoboBrowser(
    user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
    parser="html.parser",
)
browser.open("https://github.com")
root = browser.parsed
print(type(root))  # <class 'bs4.BeautifulSoup'>

html = str(root)
print(html)

# OR:
html = browser.state.response.text
print(html)
