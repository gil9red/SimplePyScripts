#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pyquery
from pyquery import PyQuery as pq


d = pq(url="https://ru.stackoverflow.com/")

css_query = (
    "#question-mini-list [data-post-id] .s-post-summary--content-title > a.s-link"
)
a_el = d(css_query)
print(repr(a_el))
titles = [a.text for a in a_el]
print(len(titles))
print(repr(titles[0]))
"""
[<a.s-link>, <a.s-link>, <a.s-link>, <a.s-link>, <a.s-link>, <a.s-link>, ...]
96
'Как убрать задержку перед запуском функции (SetInterval)'
"""

print()

css_query = (
    "#question-mini-list [data-post-id]:first .s-post-summary--content-title > a.s-link"
)
a_el = d(css_query)
print(repr(a_el))
print(repr(a_el.text()))
"""
[<a.s-link>]
'Как убрать задержку перед запуском функции (SetInterval)'
"""
