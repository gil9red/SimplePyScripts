#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вам дана последовательность строк.
Выведите строки, содержащие слово, состоящее из двух одинаковых частей (тандемный повтор).

Sample Input:
blabla is a tandem repetition
123123 is good too
go go
aaa

Sample Output:
blabla is a tandem repetition
123123 is good too

"""


# Пример использования. В консоли:
# > python main.py < in
# blabla is a tandem repetition
# 123123 is good too


if __name__ == "__main__":
    import sys
    import re

    for line in sys.stdin:
        line = line.rstrip()

        # Находим слова, в которых находим две одинаковые последовательности
        if re.search(r"\b(.+)\1\b", line):
            print(line)
