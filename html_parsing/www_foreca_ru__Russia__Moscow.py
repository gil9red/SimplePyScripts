#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import ast
import re

import requests


def preprocess_js(text: str) -> str:
    return re.sub(r'(\w+):', r'"\1":', text)


rs = requests.get('https://www.foreca.ru/Russia/Moscow')

m = re.search(r'var mgdata = (.+);', rs.text)
js_text = m.group(1)
print(js_text)
# [{d:'пн', di: 0, dl: 'Понедельник', dt: '9.8.', hi: '21:00', h: '21', s: 'n000', r: 0.00, rl: 0.00, rs: 0.00, wx: ...

js_text = preprocess_js(js_text)
print(js_text)
# [{"d":'пн', "di": 0, "dl": 'Понедельник', "dt": '9.8.', "hi": '"21":00', "h": '21', "s": 'n000', "r": 0.00, "rl" ...

items = ast.literal_eval(js_text)
for x in items:
    print(x['dl'], x['ws'], x['wd'])
"""
Понедельник 2 45
Вторник 2 45
Вторник 2 90
Вторник 3 135
Вторник 3 180
...
Суббота 3 270
Суббота 2 315
Суббота 2 270
Суббота 2 225
Воскресенье 2 225
"""
