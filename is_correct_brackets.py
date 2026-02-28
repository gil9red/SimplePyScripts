#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def is_correct_brackets(text) -> bool:
    while "()" in text or "[]" in text or "{}" in text:
        text = text.replace("()", "")
        text = text.replace("[]", "")
        text = text.replace("{}", "")

    # Возвращаем True, если text с пустой строкой
    return not text


if __name__ == "__main__":
    assert is_correct_brackets("(((())))")
    assert is_correct_brackets("(((())") is False
    assert is_correct_brackets("())))") is False
    assert is_correct_brackets("((((){}[]{}[])))")
    assert is_correct_brackets("(){}[]{}[])))") is False
    assert is_correct_brackets("(){}[]{}[]")
