#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from simple_distance import distance


def match_two_words(word_1: str, word_2: str) -> bool:
    number = distance(word_1, word_2)

    # Считаем что разница в 2 символа и меньше еще нормальная
    return number < 3


if __name__ == "__main__":
    need_word = "Привет"

    print(match_two_words("Привет", need_word))  # True
    print(match_two_words("Првет", need_word))  # True
    print(match_two_words("Прывет", need_word))  # True
    print(match_two_words("Привед", need_word))  # True
    print(match_two_words("Превед", need_word))  # True

    print(match_two_words("Преед", need_word))  # False
