#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

"""
Загадка: есть 3 вида монеток весом 7, 9 и 17 грамм.
Монеток каждого вида может быть не больше 10.
Нужно набрать монеток на 107 грамм.

И ниже приведено решение этой загадки.
"""


def find_first_selection(a, b, c, max_sum):
    """Функция вернет первый правильный вариант"""

    if max_sum == 0:
        return a, b, c

    if a == 10 and b == 10 and c == 10:
        return

    if max_sum < 0:
        return

    if a <= 10:
        r = find_first_selection(a + 1, b, c, max_sum - 7)
        if isinstance(r, tuple):
            return r

    if b <= 10:
        r = find_first_selection(a, b + 1, c, max_sum - 9)
        if isinstance(r, tuple):
            return r

    if c <= 10:
        r = find_first_selection(a, b, c + 1, max_sum - 17)
        if isinstance(r, tuple):
            return r


def find_all_selection(a, b, c, max_sum, all_sel):
    """Функция будет перебирать и запоминать все варианты"""

    if max_sum == 0:
        select = a, b, c
        if select not in all_sel:
            all_sel.append(select)

    if a == 10 and b == 10 and c == 10:
        return

    if max_sum < 0:
        return -1

    if a <= 10:
        find_all_selection(a + 1, b, c, max_sum - 7, all_sel)

    if b <= 10:
        find_all_selection(a, b + 1, c, max_sum - 9, all_sel)

    if c <= 10:
        find_all_selection(a, b, c + 1, max_sum - 17, all_sel)


if __name__ == '__main__':
    selection = find_first_selection(0, 0, 0, 107)
    print('{}*7 + {}*9 + {}*17 = 107'.format(*selection))
    print()

    print('Все варианты:')
    all_selection = []
    find_all_selection(0, 0, 0, 107, all_selection)
    for i, sel in enumerate(all_selection, 1):
        print('{}. {}*7 + {}*9 + {}*17 = 107'.format(i, *sel))
