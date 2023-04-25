#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/776780/201445


import hashlib
from itertools import product


def brute_force(mask, hsh, alphabet):
    # заменяем '*' на '{}' для последующей подстановки в 'str.format()'
    pwd_pat = mask.replace("*", "{}")

    # число звездочек - будем использовать в качестве `product(.., repeat)`
    N = mask.count("*")
    i = 0
    for chars in product(alphabet, repeat=N):
        i += 1
        if i % 10000 == 0:
            print(f"Iterations: {i}")

        if hsh == hashlib.sha256(pwd_pat.format(*chars).encode()).hexdigest():
            text = pwd_pat.format(*chars)
            print(f"Found: {text}")
            return text

    return None


if __name__ == "__main__":
    from string import ascii_letters, digits
    alphabet = ascii_letters + digits

    # Password: qwe12y
    hsh = "b8cc184b3f4aeb6adb6601ea3e39ef5ac098791acc2a505a66746f43d0c7ed85"
    print(brute_force("qw****", hsh, alphabet))
