#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def shuffle_chars_in_word(text):
    import random

    words = [list(word) for word in text.split()]
    new_words = list()
    for word in words:
        random.shuffle(word)

        new_words.append(''.join(word))

    text = ' '.join(new_words)
    return text.capitalize()


if __name__ == '__main__':
    text = "Иди нахуй!"
    print(shuffle_chars_in_word(text))
    print(shuffle_chars_in_word(text))
    print(shuffle_chars_in_word(text))
    print(shuffle_chars_in_word(text))
