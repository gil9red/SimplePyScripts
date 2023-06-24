#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Для решения головоломки в локации аэропорта из Grim Tales 9: Threads Of Destiny


from random import randrange


def is_math_magic_square(matrix) -> bool:
    # Rows
    for row in matrix:
        if sum(row) != 15:
            return False

    # Columns
    for j in range(3):
        if sum(matrix[i][j] for i in range(3)) != 15:
            return False

    # Diag top-left + bottom-right
    if matrix[0][0] + matrix[1][1] + matrix[2][2] != 15:
        return False

    # Diag top-right + bottom-left
    if matrix[0][2] + matrix[1][1] + matrix[2][0] != 15:
        return False

    return True


matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

while True:
    i1, j1 = randrange(0, 3), randrange(0, 3)
    i2, j2 = randrange(0, 3), randrange(0, 3)

    matrix[i1][j1], matrix[i2][j2] = matrix[i2][j2], matrix[i1][j1]

    if is_math_magic_square(matrix):
        break

for row in matrix:
    print(row)
