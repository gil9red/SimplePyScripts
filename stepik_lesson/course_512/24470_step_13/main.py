#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вам дана последовательность строк.
В каждой строке замените первое вхождение слова, состоящего только из латинских букв "a" (регистр не важен),
на слово "argh".

Примечание:
Обратите внимание на параметр count у функции sub﻿.

Sample Input:
There’ll be no more "Aaaaaaaaaaaaaaa"
AaAaAaA AaAaAaA

Sample Output:
There’ll be no more "argh"
argh AaAaAaA

"""


# Пример использования. В консоли:
# > python main.py < in
# There’ll be no more "argh"
# argh AaAaAaA


if __name__ == "__main__":
    import sys
    import re

    for line in sys.stdin:
        line = line.rstrip()

        print(re.sub(r"\ba+\b", "argh", line, count=1, flags=re.IGNORECASE))
