#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Morse code with Python unary + and - operators"""

# SOURCE: https://habrahabr.ru/post/349776/
# SOURCE: https://gist.github.com/Saluev/c07bef8ffa7290345b0c816fed2ca418


MORSE_ALPHABET = {
    "А": ".-",
    "Б": "-...",
    "В": ".--",
    "Г": "--.",
    "Д": "-..",
    "Е": ".",
    "Ж": "...-",
    "З": "--..",
    "И": "..",
    "Й": ".---",
    "К": "-.-",
    "Л": ".-..",
    "М": "--",
    "Н": "-.",
    "О": "---",
    "П": ".--.",
    "Р": ".-.",
    "С": "...",
    "Т": "-",
    "У": "..-",
    "Ф": "..-.",
    "Х": "....",
    "Ц": "-.-.",
    "Ч": "---.",
    "Ш": "----",
    "Щ": "--.-",
    "Ъ": "--.--",
    "Ы": "-.--",
    "Ь": "-..-",
    "Э": "..-..",
    "Ю": "..--",
    "Я": ".-.-",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": "......",
    ",": ".-.-.-",
    ":": "---...",
    ";": "-.-.-.",
    "(": "-.--.-",
    ")": "-.--.-",
    "'": ".----.",
    '"': ".-..-.",
    "-": "-....-",
    "/": "-..-.",
    "?": "..--..",
    "!": "--..--",
    "@": ".--.-.",
    "=": "-...-",
    " ": " ",
}

INVERSE_MORSE_ALPHABET = {v: k for k, v in MORSE_ALPHABET.items()}


class Morse(object):
    def __init__(self, buffer=""):
        self.buffer = buffer

    def __neg__(self):
        return Morse("-" + self.buffer)

    def __pos__(self):
        return Morse("." + self.buffer)

    def __str__(self):
        return INVERSE_MORSE_ALPHABET[self.buffer]

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return str(self) + str(+other)

    def __radd__(self, s):
        return s + str(+self)

    def __sub__(self, other):
        return str(self) + str(-other)

    def __rsub__(self, s):
        return s + str(-self)


class MorseWithSpace(Morse):
    def __str__(self):
        return super().__str__() + " "

    def __neg__(self):
        return MorseWithSpace(super().__neg__().buffer)

    def __pos__(self):
        return MorseWithSpace(super().__pos__().buffer)


def morsify(s):
    s = "_".join(map(MORSE_ALPHABET.get, s.upper()))
    s = s.replace(".", "+") + ("_" if s else "")
    s = s.replace("_ ", "__").replace(" _", "__")
    return s


if __name__ == "__main__":
    _, ___ = Morse(), MorseWithSpace()
    print(+--+_ + -+_ + +_ + --_ + _ - _ + -+-+-___ - -+_ + +_ - _ + +++_ + -_ - +++_ - -++--_)

    print(morsify("ПРИВЕТ ХАБР!"))  # +--+_+-+_++_+--_+_-___++++_+-_-+++_+-+_--++--_
    print(+--+_ + -+_ + +_ + --_ + _ - ___ + +++_ + -_ - +++_ + -+_ - -++--_)
