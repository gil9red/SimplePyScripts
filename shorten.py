#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def shorten(
    text: str,
    length: int = 30,
    middle: bool = False,
    placeholder: str = "...",
) -> str:
    if not text or len(text) <= length:
        return text

    available_len: int = length - len(placeholder)

    if middle:
        start_len: int = available_len // 2
        end_len: int = available_len - start_len

        return text[:start_len] + placeholder + text[-end_len:]

    return text[:available_len] + placeholder


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

    file_name: str = (
        r"C:\Users\ipetrash\PycharmProjects\SimplePyScripts\_FOO_TEST_TEST\FOO_TEST_TEST.py"
    )

    short_file_name: str = shorten(file_name)
    assert len(short_file_name) == 30
    assert short_file_name == r"C:\Users\ipetrash\PycharmPr..."

    short_file_name: str = shorten(file_name, middle=True)
    assert len(short_file_name) == 30
    assert short_file_name == r"C:\Users\ipet...O_TEST_TEST.py"
