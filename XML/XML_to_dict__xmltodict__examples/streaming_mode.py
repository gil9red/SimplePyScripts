#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/martinblech/xmltodict#streaming-mode


# pip install xmltodict
import xmltodict


def handle(path, item):
    print(f'path: {path} item: {item!r}')
    return True


xml_str = """\
<a prop="x">
    <b>1</b>
    <b>2</b>
</a>
"""

xmltodict.parse(xml_str, item_depth=2, item_callback=handle)
