#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def shorten(text: str, length: int = 30, placeholder: str = "...") -> str:
    if not text:
        return text

    if len(text) > length:
        text = text[: length - len(placeholder)] + placeholder
    return text


if __name__ == "__main__":
    text = "1234" * 20
    new_text = shorten(text)
    assert new_text == "123412341234123412341234123..."

    text = "12345"
    new_text = shorten(text, length=5)
    assert new_text == "12345"

    text = "123"
    new_text = shorten(text, length=5)
    assert new_text == "123"

    text = "1234567890"
    new_text = shorten(text, length=7)
    assert new_text == "1234..."

    text = "12356"
    new_text = shorten(text, length=3)
    assert new_text == "..."
