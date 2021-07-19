#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import goslate
gs = goslate.Goslate()


text = gs.translate('Привет мир!', 'en')
print(text)
assert text == 'Hello World!'
