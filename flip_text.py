#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://olegon.ru/pr/flip.html
FLIP_TABLE = {
    "a": "\u0250",
    "b": "q",
    "c": "\u0254",
    "d": "p",
    "e": "\u01DD",
    "f": "\u025F",
    "g": "\u0183",
    "h": "\u0265",
    "i": "\u0131",
    "j": "\u027E",
    "k": "\u029E",
    "m": "\u026F",
    "n": "u",
    "r": "\u0279",
    "t": "\u0287",
    "v": "\u028C",
    "w": "\u028D",
    "y": "\u028E",
    ".": "\u02D9",
    "[": "]",
    "(": ")",
    "{": "}",
    "?": "\u00BF",
    "!": "\u00A1",
    "'": ",",
    "<": ">",
    "_": "\u203E",
    "\u203F": "\u2040",
    "\u2045": "\u2046",
    "\u2234": "\u2235",
    "\r": "\n",
    "а": "ɐ",
    "б": "ƍ",
    "в": "ʚ",
    "г": "ɹ",
    "д": "ɓ",
    "е": "ǝ",
    "ё": "ǝ",
    "ж": "ж",
    "з": "ε",
    "и": "и",
    "й": "ņ",
    "к": "ʞ",
    "л": "v",
    "м": "w",
    "н": "н",
    "о": "о",
    "п": "u",
    "р": "d",
    "с": "ɔ",
    "т": "ɯ",
    "у": "ʎ",
    "ф": "ф",
    "х": "х",
    "ц": "ǹ",
    "ч": "Һ",
    "ш": "m",
    "щ": "m",
    "ъ": "q",
    "ы": "ıq",
    "ь": "q",
    "э": "є",
    "ю": "oı",
    "я": "ʁ",
}


def flip_text(text, reverse=True):
    new_text = [FLIP_TABLE.get(c, c) for c in text.lower()]

    if reverse:
        new_text.reverse()

    return "".join(new_text)


if __name__ == "__main__":
    text = "Перевернутый текст!"
    print(flip_text(text))  # ¡ɯɔʞǝɯ ņıqɯʎнdǝʚǝdǝu
    print(flip_text(text, reverse=False))  # uǝdǝʚǝdнʎɯıqņ ɯǝʞɔɯ¡
