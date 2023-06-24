#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def invert_number(number: int) -> int:
    """
    number: 7 = 0b111 -> 0b000 = 0
    number: 111 = 0b1101111 -> 0b0010000 = 16
    number: 10000000000 = 0b1001010100000010111110010000000000 -> 0b0110101011111101000001101111111111 = 7179869183

    :param number
    :return: invert number
    """

    return int("".join("1" if i == "0" else "0" for i in bin(number)[2:]), base=2)


if __name__ == "__main__":
    print(invert_number(0))
    print(invert_number(1))
    print(invert_number(7))
    print(invert_number(111))
    print(invert_number(10**10))

    assert invert_number(0) == 1
    assert invert_number(1) == 0
    assert invert_number(7) == 0
    assert invert_number(111) == 16
    assert invert_number(10**10) == 7179869183
