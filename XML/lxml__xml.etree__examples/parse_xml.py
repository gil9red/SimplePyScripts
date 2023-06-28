#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from lxml import etree


root = etree.fromstring("<a><b>Hello</b><c>world!</c></a>")

print(etree.tostring(root))  # b'<a><b>Hello</b><c>world!</c></a>'
print(etree.tostring(root, encoding="unicode"))  # <a><b>Hello</b><c>world!</c></a>
print(
    etree.tostring(root, pretty_print=True)
)  # b'<a>\n  <b>Hello</b>\n  <c>world!</c>\n</a>\n'
print(etree.tostring(root, encoding="unicode", pretty_print=True))
# <a>
#   <b>Hello</b>
#   <c>world!</c>
# </a>
