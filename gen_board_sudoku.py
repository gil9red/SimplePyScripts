#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# http://habrahabr.ru/post/192102/
# http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html


def gen_sudoku(n=3):
    return [
        [((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)]
        for i in range(n * n)
    ]


for row in gen_sudoku():
    print(row)
