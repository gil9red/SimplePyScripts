#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://ru.stackoverflow.com/q/1270426/201445


import configparser


dict1 = [
    {'object': 'label', 'icon': 'icon', 'icon_hover': 'icon_hover', 'command': 'command'},
    {'object': 'button', 'icon': 'icon', 'icon_hover': 'icon_hover', 'command': 'command'},
    {'object': 'color', 'icon': 'icon', 'icon_hover': 'icon_hover', 'command': 'command'},
    {'object': 'line', 'icon': 'icon', 'icon_hover': 'icon_hover', 'command': 'command'},
    {'object': 'unknown', 'icon': 'icon', 'icon_hover': 'icon_hover', 'command': 'command'},
]

config = configparser.ConfigParser()

for d in dict1:
    config[d['object']] = d

with open('example.ini', 'w') as f:
    config.write(f)
