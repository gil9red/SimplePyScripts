#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from bs4 import BeautifulSoup


# SOURCE: https://stackoverflow.com/a/15513483/5909792
orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


BeautifulSoup.prettify = prettify


def process_html_string(text: str) -> str:
    """
    Функция из текста выдирает строку с html. Она должна начинаться на < и заканчиваться >

    """

    start = text.index('<')
    end = text.rindex('>')
    return text[start:end + 1]


def pretty_html(text: str) -> str:
    text = process_html_string(text)
    root = BeautifulSoup(text, 'html.parser')
    return root.prettify()


if __name__ == '__main__':
    text = '<html><br><b/><c><z/><br/><h/></c></html>'
    print(pretty_html(text))
