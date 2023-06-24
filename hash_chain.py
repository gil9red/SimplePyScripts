#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://en.wikipedia.org/wiki/Hash_chain


import hashlib


def get_hash(text):
    sha256 = hashlib.sha256(text.encode("utf-8"))
    return sha256.hexdigest()


def hash_chain(text, number=1):
    for _ in range(number):
        text = get_hash(text)

    return text


if __name__ == "__main__":
    text = "Hello World!"
    print("Text:", text)

    # A hash chain is a successive application of a cryptographic hash function h to a string x x.
    # For example, h(h(h(h(x)))) gives a hash chain of length 4, often denoted h^{4}(x)
    h = get_hash
    print("hash chain (5):", h(h(h(h(h(text))))))
    print("\n")

    print("hash_chain")

    hash_text = hash_chain(text)
    print("hash_chain(1):", hash_text)
    print()

    hash_text = hash_chain(text, number=4)
    print("hash_chain(4):", hash_text)

    hash_text = hash_chain(hash_text)
    print("hash_chain(4+1):", hash_text)
    print()

    hash_text = hash_chain(text, number=5)
    print("hash_chain(5):", hash_text)
