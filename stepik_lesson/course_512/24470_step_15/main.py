#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вам дана последовательность строк.
В каждой строке замените все вхождения нескольких одинаковых букв на одну букву.
Буквой считается символ из группы \w.

Sample Input:
attraction
buzzzz

Sample Output:
atraction
buz

"""


# Пример использования. В консоли:
# > python main.py < in
# atraction
# buz


if __name__ == "__main__":
    import sys
    import re

    for line in sys.stdin:
        line = line.rstrip()

        # Ищем буквенный символ и группу повторяющих его символов и заменяем их самим символом
        print(re.sub(r"(\w)(\1)+", r"\1", line))
