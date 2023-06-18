#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def solution(roman):
    roman_by_arabic = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    total_number = 0
    last_num = -1

    for c in reversed(roman):
        current_number = roman_by_arabic[c]

        if current_number >= last_num:
            total_number += current_number
        else:
            total_number -= current_number

        last_num = current_number

    return total_number


if __name__ == "__main__":
    assert solution("XXI") == 21
    assert solution("XIX") == 19
    assert solution("MDCLXVI") == 1666
