#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys


# Don't let the machines win. You are humanity's last hope...

width = int(input())  # the number of cells on the X axis
height = int(input())  # the number of cells on the Y axis

# print("width: {}, height: {}".format(width, height), file=sys.stderr)

matrix = list()

for i in range(height):
    line = input()  # width characters, each either 0 or .
    print("line: {}".format(line), file=sys.stderr)

    matrix.append(list(line))

print("matrix:\n{}".format(matrix), file=sys.stderr)


# Ищем соседей справа
def right_neighbor(matrix, i, j):
    for _j in range(j + 1, width):
        if matrix[i][_j] == "0":
            return _j, i

    return -1, -1


# Ищем соседей снизу
def bottom_neighbor(matrix, i, j):
    for _i in range(i + 1, height):
        if matrix[_i][j] == "0":
            return j, _i

    return -1, -1


for i in range(height):
    for j in range(width):
        if matrix[i][j] == ".":
            continue

        x2, y2 = right_neighbor(matrix, i, j)
        x3, y3 = bottom_neighbor(matrix, i, j)

        # Three coordinates: a node, its right neighbor, its bottom neighbor
        # print(i, j, x2, y2, x3, y3, file=sys.stderr)
        print(j, i, x2, y2, x3, y3)
