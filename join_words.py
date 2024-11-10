#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def join_words(word_1: str, word_2: str) -> str:
    result: str = word_1 + word_2
    for i in range(min(len(word_1), len(word_2))):
        if word_1[-i:].upper() == word_2[:i].upper():
            result = word_1.removesuffix(word_1[-i:]) + word_2

    return result


if __name__ == "__main__":
    result = join_words("Капитан", "АНИМЕ")
    print(result)
    assert result == "КапитАНИМЕ"
