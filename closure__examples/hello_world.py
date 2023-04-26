#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.wikipedia.org/wiki/Замыкание_(программирование)


# multiplier возвращает функцию умножения на n
def multiplier(n):
    def mul(k):
        return n * k

    return mul


# mul3 - функция, умножающая на 3
mul3 = multiplier(3)
print(mul3(3), mul3(5))  # 9 15
