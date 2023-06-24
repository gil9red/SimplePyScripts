#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from string import ascii_lowercase


def text_from_num_alp_sequence(sequence):
    """[8, 1, 16, 16, 25, ' ', 14, 15, 23, ' ', 1, 18, 9, 5, 12, '?'] -> happy now ariel?"""

    text = ""
    for c in sequence:
        text += c if isinstance(c, str) else ascii_lowercase[c - 1]

    return text


if __name__ == "__main__":
    # 16 серия
    sequence = [
        2,
        21,
        20,
        " ",
        23,
        8,
        16,
        " ",
        19,
        20,
        15,
        12,
        5,
        " ",
        20,
        8,
        5,
        " ",
        3,
        1,
        16,
        5,
        18,
        19,
        "?",
    ]
    text = text_from_num_alp_sequence(sequence)
    print(text)
    # but whp stole the capers?

    # 17 серия
    sequence = [8, 1, 16, 16, 25, " ", 14, 15, 23, " ", 1, 18, 9, 5, 12, "?"]
    text = text_from_num_alp_sequence(sequence)
    print(text)
    # happy now ariel?

    # 18 серия
    sequence = [
        9,
        20,
        " ",
        23,
        15,
        18,
        11,
        19,
        " ",
        6,
        15,
        18,
        " ",
        16,
        9,
        9,
        9,
        9,
        9,
        9,
        9,
        7,
        19,
        "!",
    ]
    text = text_from_num_alp_sequence(sequence)
    print(text)
    # it works for piiiiiiigs!

    # 19 серия
    sequence = [20, 15, " ", 2, 5, " ", 3, 15, 14, 20, 9, 14, 21, 5, 4, "..."]
    text = text_from_num_alp_sequence(sequence)
    print(text)
    # to be continued...
