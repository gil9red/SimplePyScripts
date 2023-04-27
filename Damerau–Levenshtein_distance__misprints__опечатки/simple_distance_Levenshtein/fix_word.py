#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from simple_distance import distance


def fix_word(word: str, need_word: str) -> str | None:
    number = distance(word, need_word)

    # Считаем что разница в 2 символа и меньше еще нормальная
    if number >= 3:
        return

    return need_word


if __name__ == "__main__":
    need_word = "Привет"

    print(fix_word("Привет", need_word))  # Привет
    print(fix_word("Првет", need_word))  # Привет
    print(fix_word("Прывет", need_word))  # Привет
    print(fix_word("Привед", need_word))  # Привет
    print(fix_word("Превед", need_word))  # Привет

    print(fix_word("Преед", need_word))  # None
