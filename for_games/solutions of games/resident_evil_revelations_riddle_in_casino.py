#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Загадка: есть 3 вида монеток весом 7, 9 и 17 грамм.
Монеток каждого вида может быть не больше 10.
Нужно набрать монеток на 107 грамм.

И ниже приведено решение этой загадки.
"""


def find_first_selection(
    a: int,
    b: int,
    c: int,
    max_sum: int,
) -> tuple[int, int, int] | None:
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


def find_all_selection(
    a: int,
    b: int,
    c: int,
    max_sum: int,
    all_sel: list[tuple[int, int, int]],
):
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


if __name__ == "__main__":
    a, b, c = find_first_selection(0, 0, 0, 107)
    print(f"{a}*7 + {b}*9 + {c}*17 = 107")
    # 9*7 + 3*9 + 1*17 = 107

    print()

    print("Все варианты:")
    all_selection = []
    find_all_selection(0, 0, 0, 107, all_selection)
    for i, (a, b, c) in enumerate(all_selection, 1):
        print(f"{i}. {a}*7 + {b}*9 + {c}*17 = 107")
    """
    Все варианты:
    1. 9*7 + 3*9 + 1*17 = 107
    2. 8*7 + 0*9 + 3*17 = 107
    3. 5*7 + 8*9 + 0*17 = 107
    4. 4*7 + 5*9 + 2*17 = 107
    5. 3*7 + 2*9 + 4*17 = 107
    6. 0*7 + 10*9 + 1*17 = 107
    """
