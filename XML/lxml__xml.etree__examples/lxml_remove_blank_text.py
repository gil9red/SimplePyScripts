#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from lxml import etree


data: bytes = b"<a>\r\n<b>Hello</b>\r\n<c>\r\nworld\r\n\r\n!</c>\r\n</a>"

root = etree.fromstring(data)
result: bytes = etree.tostring(root)
print(result)
# b'<a>\n<b>Hello</b>\n<c>\nworld\n\n!</c>\n</a>'

assert result == b'<a>\n<b>Hello</b>\n<c>\nworld\n\n!</c>\n</a>'

print()

root = etree.fromstring(
    text=data,
    parser=etree.XMLParser(remove_blank_text=True),
)
result: bytes = etree.tostring(root)
print(result)
# b'<a><b>Hello</b><c>\nworld\n\n!</c></a>'

assert result == b'<a><b>Hello</b><c>\nworld\n\n!</c></a>'
