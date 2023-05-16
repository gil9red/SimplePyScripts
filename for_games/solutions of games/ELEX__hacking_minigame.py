#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random


# Этот шаблон допускает любые числа
_ = "*"
keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
fixed_values = [_, _, _, _]
need_values = []

keys = [1, 2, 4, 5, 7, 8, 9]
keys = [0, 1, 6, 8]
keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

eval_template = "a == b and (a > c < d)"
eval_template = "a > b > c < d"
eval_template = "a > b < c > d"

fixed_values = [_, _, _, _]
fixed_values = [_, 1, 8, _]

need_values = [4]

while True:
    items = keys.copy()
    fixed_items = fixed_values.copy()
    need_items = need_values.copy()

    # Удаляем дублирующие значения
    for fixed in fixed_items:
        if fixed in items:
            items.remove(fixed)

        if fixed in need_items:
            need_items.remove(fixed)

    random.shuffle(items)
    random.shuffle(need_items)

    free_idx = [i for i, x in enumerate(fixed_items) if x == _]
    random.shuffle(free_idx)

    for i in free_idx:
        # Если есть обязательные значения, то берем из них
        if need_items:
            fixed_items[i] = need_items.pop()
        else:
            fixed_items[i] = items.pop()

    a, b, c, d = fixed_items

    text = (
        eval_template.replace("a", str(a))
        .replace("b", str(b))
        .replace("c", str(c))
        .replace("d", str(d))
    )

    ok = eval(text)
    if ok:
        print(text)
        break
