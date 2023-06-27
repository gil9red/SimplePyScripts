#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вам дается текстовый файл, содержащий некоторое количество непустых строк.
На основе него сгенерируйте новый текстовый файл, содержащий те же строки в обратном порядке.

Пример входного файла:
ab
c
dde
ff

Пример выходного файла:
ff
dde
c
ab
"""


if __name__ == "__main__":
    with open("dataset_24465_4.txt") as f:
        lines = reversed(f.readlines())

        with open("reverse_dataset_24465_4.txt", "w") as f:
            for line in lines:
                print(line, file=f, end="")
