#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stepik.org/lesson/349848/step/1?unit=333703


import random
import string


DIGITS = string.digits
LOWERCASE_LETTERS = string.ascii_lowercase
UPPERCASE_LETTERS = string.ascii_uppercase
PUNCTUATION = "!#$%&*+-=?@^_"
AMBIGUOUS_CHARACTERS = "il1Lo0O"


def generate_password_from_string(
    length: int = 8,
    chars: str | list[str] = DIGITS
    + LOWERCASE_LETTERS
    + UPPERCASE_LETTERS
    + PUNCTUATION,
) -> str:
    return "".join(random.choices(chars, k=length))


def generate_password(
    length: int = 8,
    digits_on=True,
    uppers_on=True,
    lowers_on=True,
    puncts_on=True,
    ambiguous_on=False,
) -> str:
    chars = []

    if digits_on:
        chars += DIGITS

    if uppers_on:
        chars += UPPERCASE_LETTERS

    if lowers_on:
        chars += LOWERCASE_LETTERS

    if puncts_on:
        chars += PUNCTUATION

    if not ambiguous_on:
        for c in AMBIGUOUS_CHARACTERS:
            chars.remove(c)

    return generate_password_from_string(length, chars)


def input_get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid int!")


def input_get_bool(prompt: str) -> bool:
    while True:
        result = input(prompt).lower()
        return result in ["y", "yes", "да"]


if __name__ == "__main__":
    print(generate_password())
    print()

    number_pwd = input_get_int("Specify the number of passwords to generate: ")
    len_pwd = input_get_int("Specify the length of one password: ")
    digits_on = input_get_bool("Should the digits (0-9) be included? (y/n): ")
    uppers_on = input_get_bool("Do uppercase letters (A-Z) be included? (y/n): ")
    lowers_on = input_get_bool("Whether to include lowercase letters (a-z)? (y/n): ")
    puncts_on = input_get_bool(
        "Should the characters (!#$%&*+-=?@^_) be included? (y/n): "
    )
    ambiguous_on = input_get_bool(
        "Whether to exclude ambiguous characters (il1Lo0O)? (y/n): "
    )

    for _ in range(number_pwd):
        print(
            generate_password(
                len_pwd, digits_on, uppers_on, lowers_on, puncts_on, ambiguous_on
            )
        )
