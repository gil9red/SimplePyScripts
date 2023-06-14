#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
from pathlib import Path


file_name = Path(__file__).parent / "abusive words.txt"
with open(file_name, encoding="utf-8") as f:
    WORDS = f.readlines()


def get_words(number, chain_length=2):
    random.shuffle(WORDS)
    random_words = list(map(str.strip, WORDS[: number * chain_length]))

    words = []
    for i in range(0, len(random_words), chain_length):
        chain = random_words[i : i + chain_length]
        chain[0] = chain[0].title()
        words.append(" ".join(chain))

    return words


if __name__ == "__main__":
    print(*get_words(10), sep="\n")
