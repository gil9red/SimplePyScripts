#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def compress(text):
    """ Функция для сжатия текста, с повторяющимися последовательностями символов

    aaaa        -> 4a
    aaaabbbbb   -> 4a5b
    aabcDDfaaaa -> 2abc2Df4a

    """

    chars = list()

    import itertools
    for char, same in itertools.groupby(text):
        count = sum(1 for _ in same)  # number of repetitions
        chars.append(char if count == 1 else str(count) + char)

    return ''.join(chars)


if __name__ == '__main__':
    print(compress("aaaa"))
    print(compress("aaaabbbbb"))
    print(compress("aabcDDfaaaa"))
