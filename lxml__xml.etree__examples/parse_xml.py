#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from lxml import etree
root = etree.fromstring('<a><b>Hello</b><c>world!</c></a>')

print(etree.tostring(root))                      # b'<a><b>Hello</b><c>world!</c></a>'
print(etree.tostring(root, encoding='unicode'))  # <a><b>Hello</b><c>world!</c></a>
