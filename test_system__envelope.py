#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from contextlib import redirect_stdout
from io import StringIO


# Заданы размеры envelop_x, envelop_y - размеры конверта и x, y листа бумаги (все размеры
# могут быть в диапазоне от 1 до 1000)
#
# Определить, поместится ли бумага в конверте (стороны листа параллельны сторонам конверта)
#
# Результат проверки вывести на консоль (ДА/НЕТ)
# Использовать только операторы if/elif/else, можно вложенные


envelop_x, envelop_y = 10, 7
print(f'envelop_x={envelop_x}, envelop_y={envelop_y}')
items = [
    [9, 8, "НЕТ"], [6, 8, "ДА"], [8, 6, "ДА"],
    [3, 4, "ДА"], [11, 9, "НЕТ"], [9, 11, "НЕТ"]
]


def check_1(x, y):
    if envelop_x > x and envelop_y > y:
        print('ДА')
    elif envelop_y > x and envelop_x > y:
        print('ДА')
    else:
        print('НЕТ')


for x, y, expected in items:
    f = StringIO()

    with redirect_stdout(f):
        check_1(x, y)

    actual = f.getvalue().strip().upper()
    ok = actual != expected
    if ok:
        print(f'{x}, {y}. expected: {expected}, actual: {actual}')


print()


# Усложненное задание, решать по желанию.
# Заданы размеры hole_x, hole_y прямоугольного отверстия и размеры х, у, z кирпича (все размеры
# могут быть в диапазоне от 1 до 1000)
#
# Определить, пройдет ли кирпич через отверстие (грани кирпича параллельны сторонам отверстия)

hole_x, hole_y = 8, 9
print(f'hole_x={hole_x}, hole_y={hole_y}')
items = [
    [11, 10, 2, "НЕТ"], [11, 2, 10, "НЕТ"], [10, 11, 2, "НЕТ"],
    [10, 2, 11, "НЕТ"], [2, 10, 11, "НЕТ"], [2, 11, 10, "НЕТ"],
    [3, 5, 6, "ДА"], [3, 6, 5, "ДА"], [6, 3, 5, "ДА"],
    [6, 5, 3, "ДА"], [5, 6, 3, "ДА"], [5, 3, 6, "ДА"],
    [11, 3, 6, "ДА"], [11, 6, 3, "ДА"], [6, 11, 3, "ДА"],
    [6, 3, 11, "ДА"], [3, 6, 11, "ДА"], [3, 11, 6, "ДА"]
]


def check_2(x, y, z):
    if hole_x > x and hole_y > y:
        print('ДА')
    elif hole_x > y and hole_y > x:
        print('ДА')
    elif hole_x > x and hole_y > z:
        print('ДА')
    elif hole_x > z and hole_y > x:
        print('ДА')
    elif hole_x > z and hole_y > y:
        print('ДА')
    elif hole_x > y and hole_y > z:
        print('ДА')
    else:
        print('НЕТ')


for x, y, z, expected in items:
    f = StringIO()

    with redirect_stdout(f):
        check_2(x, y, z)

    actual = f.getvalue().strip().upper()
    ok = actual != expected
    if ok:
        print(f'{x}, {y}, {z}. expected: {expected}, actual: {actual}')
