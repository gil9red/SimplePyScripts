#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Fingerprinting with Zero-Width Characters

# zero-width-detection
# https://medium.com/@umpox/be-careful-what-you-copy-invisibly-inserting-usernames-into-text-with-zero-width-characters-18b4e6f17b66
# https://habrahabr.ru/post/352950/

# https://github.com/umpox/zero-width-detection
# DEMO: https://umpox.github.io/zero-width-detection/

# SOURCE: https://github.com/umpox/zero-width-detection/blob/master/src/utils/usernameToZeroWidth.js
# SOURCE: https://github.com/umpox/zero-width-detection/blob/master/src/utils/zeroWidthToUsername.js

# SOURCE: https://habrahabr.ru/post/352950/#comment_10745120
# const zeroWidthSpace = '\u200B';        // 8203
# const zeroWidthNonJoiner = '\u200C';    // 8204
# const zeroWidthJoiner = '\u200D';       // 8205
# const zeroWidthNoBreakSpace = '\uFEFF'; // 65279


ZERO_WIDTH_SPACE = "\u200B"  # 8203
ZERO_WIDTH_NON_JOINER = "\u200C"  # 8204
ZERO_WIDTH_JOINER = "\u200D"  # 8205
ZERO_WIDTH_NO_BREAK_SPACE = "\uFEFF"  # 65279


def to_binary(c: str) -> str:
    return bin(ord(c))[2:].zfill(8)


def text_to_binary(username: str) -> str:
    return " ".join(map(to_binary, username))


def binary_to_zero_width(binary_username: str) -> str:
    zero_width_items = []

    for c in binary_username:
        if c == "1":
            zero_width = ZERO_WIDTH_SPACE
        elif c == "0":
            zero_width = ZERO_WIDTH_NON_JOINER
        else:
            zero_width = ZERO_WIDTH_JOINER

        zero_width_items.append(zero_width)

    return ZERO_WIDTH_NO_BREAK_SPACE.join(zero_width_items)


def username_to_zero_width(username: str) -> str:
    binary_username = text_to_binary(username)
    zero_width_username = binary_to_zero_width(binary_username)
    return zero_width_username


def append_fingerprint_to_text(text: str, username: str) -> str:
    left_half = len(text) // 2
    return text[:left_half] + username_to_zero_width(username) + text[left_half:]


def zero_width_to_binary(text: str) -> str:
    binary = []

    for c in text.split(ZERO_WIDTH_NO_BREAK_SPACE):
        if c == ZERO_WIDTH_SPACE:
            binary.append("1")
        elif c == ZERO_WIDTH_NON_JOINER:
            binary.append("0")
        else:
            binary.append(" ")

    return "".join(binary)


def binary_to_text(text: str) -> str:
    return "".join(chr(int(num, 2)) for num in text.split(" "))


def get_zero_width_from_text(text: str) -> str:
    return "".join(
        c
        for c in text
        if c in (
            ZERO_WIDTH_SPACE,
            ZERO_WIDTH_NON_JOINER,
            ZERO_WIDTH_JOINER,
            ZERO_WIDTH_NO_BREAK_SPACE,
        )
    )


def get_username_from_zero_width_username(zero_width_username: str) -> str:
    binary_username = zero_width_to_binary(zero_width_username)
    text_username = binary_to_text(binary_username)
    return text_username


def get_username_from_text(text: str) -> str:
    zero_width_username = get_zero_width_from_text(text)
    binary_username = zero_width_to_binary(zero_width_username)
    text_username = binary_to_text(binary_username)
    return text_username


if __name__ == "__main__":
    text = (
        "This is some confidential text that you really shouldn't be sharing anywhere else. "
        "Это конфиденциальный текст, которым вы действительно не должны делиться."
    )
    username = "hello world/привет мир"

    print(len(text), text)

    text_zero_width = append_fingerprint_to_text(text, username)
    print(len(text_zero_width), text_zero_width)
    print(repr(text_zero_width))
    print()

    zero_width_username_1 = username_to_zero_width(username)
    zero_width_username_2 = get_zero_width_from_text(text_zero_width)
    print(zero_width_username_1 == zero_width_username_2)
    print()

    user_name = get_username_from_zero_width_username(zero_width_username_2)
    print(user_name)

    user_name = get_username_from_text(text_zero_width)
    print(user_name)
