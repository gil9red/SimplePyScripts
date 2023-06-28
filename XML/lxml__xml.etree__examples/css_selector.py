#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from lxml import html


root = html.fromstring("<p>Hello<br><b>world</b>!</p><br>")

word = root.cssselect("b")[0]
print(html.tostring(word, encoding="unicode", with_tail=False))  # <b>world</b>
