#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def make_transliterate(text: str) -> str:
    symbols = (
        "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
        "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA",
    )
    tr = {ord(a): ord(b) for a, b in zip(*symbols)}
    return text.translate(tr)


if __name__ == "__main__":
    assert make_transliterate("Привет мир!") == "Privet mir!"

    print(make_transliterate("Hello World!"))
    print(make_transliterate("Привет мир!"))
    print(make_transliterate("Hello World! Привет мир!"))
    print(make_transliterate("Привет мир! Hello World!"))
