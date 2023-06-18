#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.wikipedia.org/wiki/Кодирование_длин_серий
# SOURCE: https://en.wikipedia.org/wiki/Run-length_encoding


import itertools


def compress(text):
    """
    Функция для сжатия текста, с повторяющимися последовательностями символов

    aaaa        -> 4a
    aaaabbbbb   -> 4a5b
    aabcDDfaaaa -> 2abc2Df4a

    """

    chars = list()

    for char, same in itertools.groupby(text):
        count = len(tuple(same))  # number of repetitions
        chars.append(char if count == 1 else str(count) + char)

    return "".join(chars)


if __name__ == "__main__":
    print(compress("aaaa"))
    print(compress("aaaabbbbb"))
    print(compress("aabcDDfaaaa"))
