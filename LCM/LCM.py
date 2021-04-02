#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# EN: Least Common Multiple.
# RU: Наименьшее общее кратное (НОК).


def gcd(a, b):
    """Нахождение НОД"""
    while a != 0:
        a, b = b % a, a  # Параллельное определение
    return b


if __name__ == '__main__':
    a, b = 7006652, 112307574
    print("LCM: %s" % ((a * b) // gcd(a, b)))

    import math
    print("LCM: %s" % ((a * b) // math.gcd(a, b)))
