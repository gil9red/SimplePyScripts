#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from multiprocessing import Pool
from multiprocessing__QApplication__in_other_process import go


if __name__ == '__main__':
    with Pool() as p:
        p.map(go, ['Alice', 'Bob', 'World'])
