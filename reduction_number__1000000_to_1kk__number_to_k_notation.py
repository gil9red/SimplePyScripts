#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def number_to_k_notation(number: int) -> str:
    k = 0

    while True:
        if number // 1000 == 0:
            break

        number /= 1000
        k += 1

    return str(round(number)) + "k" * k


if __name__ == "__main__":
    print(number_to_k_notation(123))
    assert number_to_k_notation(123) == "123"

    print(number_to_k_notation(1000))
    assert number_to_k_notation(1000) == "1k"

    print(number_to_k_notation(10000))
    assert number_to_k_notation(10000) == "10k"

    print(number_to_k_notation(5432))
    assert number_to_k_notation(5432) == "5k"

    print(number_to_k_notation(5555))
    assert number_to_k_notation(5555) == "6k"

    print(number_to_k_notation(12345))
    assert number_to_k_notation(12345) == "12k"

    print(number_to_k_notation(14288))
    assert number_to_k_notation(14288) == "14k"

    print(number_to_k_notation(21907))
    assert number_to_k_notation(21907) == "22k"

    print(number_to_k_notation(1234567890))
    assert number_to_k_notation(1234567890) == "1kkk"
