#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from multiprocessing import Pool
    from multiprocessing__QApplication__in_other_process import go

    with Pool() as p:
        p.map(go, ['Alice', 'Bob', 'World'])
