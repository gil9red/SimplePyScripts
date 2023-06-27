#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вам дана последовательность строк.
В каждой строке поменяйте местами две первых буквы в каждом слове, состоящем хотя бы из двух букв.
Буквой считается символ из группы \w﻿.

Sample Input:
this is a text
"this' !is. ?n1ce,

Sample Output:
htis si a etxt
"htis' !si. ?1nce,

"""


# Пример использования. В консоли:
# > python main.py < in
# htis si a etxt
# "htis' !si. ?1nce,


if __name__ == "__main__":
    import sys
    import re

    for line in sys.stdin:
        line = line.rstrip()

        # Ищем слова с хотя бы двумя символами, запоминаем первый символ, второй и все остальные
        # При замене сначала вставляем второй символ, потом первый, и потом все остальные
        print(re.sub(r"\b(\w)(\w)(\w*?)\b", r"\2\1\3", line))
