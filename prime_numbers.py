#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def get_prime_numbers(max_num):
    """
    Sieve of Eratosthenes algorithm.

    """

    sieve = [True] * max_num

    # Zero and one are not prime numbers
    sieve[0] = False
    sieve[1] = False

    # Create the sieve
    import math
    for i in range(2, int(math.sqrt(max_num)) + 1):
        pointer = i * 2

        while pointer < max_num:
            sieve[pointer] = False
            pointer += i

    return [i for i in range(max_num) if sieve[i]]


if __name__ == '__main__':
    assert get_prime_numbers(10) == [2, 3, 5, 7]
    assert get_prime_numbers(100) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
                                      43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
