#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os.path

file_name = os.path.join(os.path.dirname(__file__), 'abusive words.txt')
WORDS = open(file_name, encoding='utf-8').readlines()


def get_words(number, chain_length=2):
    import random
    random.shuffle(WORDS)

    random_words = list(map(str.strip, WORDS[:number * chain_length]))

    words = list()

    for i in range(0, len(random_words), chain_length):
        chain = random_words[i: i + chain_length]
        chain[0] = chain[0].title()
        words.append(' '.join(chain))

    return words


if __name__ == '__main__':
    print(*get_words(10), sep='\n')
