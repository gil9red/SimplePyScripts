#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


ITEMS = [
    ...
]

text = ''

for name in ITEMS:
    text += f"""\
          <License Name="{name}">
            <RequiredModules/>
          </License>
"""

print(text)
