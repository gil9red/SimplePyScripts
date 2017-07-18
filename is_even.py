#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def is_even(num):
    return num % 2 == 0


def is_even_2(num):
    return num & 1 == 0


for i in range(10):
    print('{} is even: {}, {}'.format(i, is_even(i), is_even_2(i)))
