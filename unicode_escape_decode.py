#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import codecs


text = "\u041e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442 \u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440 (username)"

print(codecs.unicode_internal_decode(text)[0])
# Отсутствует обязательный параметр (username)
