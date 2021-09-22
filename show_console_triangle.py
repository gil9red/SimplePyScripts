#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def print_triangle(n):
    """
    n = 5

    *
   ***
  *****
 *******
*********

    """

    starts = 1

    for i in range(1, n + 1):
        fill = ' ' * (n - i)
        print(fill + '*' * starts + fill)
        starts += 2


if __name__ == '__main__':
    print_triangle(5)
