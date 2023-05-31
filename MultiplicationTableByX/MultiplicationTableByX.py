#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Реализовать функцию-генератор строки с таблицей умножения на число Х.


if __name__ == "__main__":
    x = int(input("Input x: "))
    print(" ".join(f"{i * x}" for i in range(1, 10 + 1)))
