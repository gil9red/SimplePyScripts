#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random


keys = [2, 3, 7, 8]
keys = [1, 2, 3, 4, 5, 6, 7, 8, 9] * 2
keys = [1, 2, 3, 4, 5, 6, 7, 8, 9]
keys = [2, 3, 5, 7] * 2

eval_template = '{a} == {b} and ({a} > {c} < {d})'
eval_template = '{a} > {b} < {c} > {d}'

while True:
    items = keys.copy()
    random.shuffle(items)

    a, b, c, d = items.pop(), items.pop(), items.pop(), items.pop()
    text = eval_template.format(a=a, b=b, c=c, d=d)

    ok = eval(text)
    if ok:
        print(text)
        break
