#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://docs.python.org/3.6/library/multiprocessing.html


from multiprocessing import Pool


def f(x):
    return x * x


if __name__ == '__main__':
    with Pool(5) as p:
        result = p.map(f, [1, 2, 3])
        print(result)  # [1, 4, 9]
