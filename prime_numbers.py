#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/3035188/5909792


def get_prime_numbers(n: int) -> list[int]:
    """Returns a list of primes < n"""

    sieve = [True] * n
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i : : 2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


if __name__ == "__main__":
    assert get_prime_numbers(10) == [2, 3, 5, 7]
    assert get_prime_numbers(100) == [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
        43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
    ]

    print(sum(get_prime_numbers(2_000_000)))
    assert sum(get_prime_numbers(2_000_000)) == 142913828922
