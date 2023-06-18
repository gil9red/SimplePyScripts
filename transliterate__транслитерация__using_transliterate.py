#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/barseghyanartur/transliterate
import transliterate


def make_transliterate(text: str) -> str:
    try:
        return transliterate.translit(text, reversed=True)
    except transliterate.exceptions.LanguageDetectionError:
        return text


if __name__ == "__main__":
    assert make_transliterate("Привет мир!") == "Privet mir!"

    print(make_transliterate("Hello World!"))
    print(make_transliterate("Привет мир!"))
    print(make_transliterate("Hello World! Привет мир!"))
    print(make_transliterate("Привет мир! Hello World!"))
