#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    words = open('abusive words.txt', encoding='utf-8').readlines()

    import random
    random.shuffle(words)

    ten_words = list(map(str.strip, words[:10]))
    for i in range(0, len(ten_words), 2):
        print(ten_words[i].title(), ten_words[i + 1])
