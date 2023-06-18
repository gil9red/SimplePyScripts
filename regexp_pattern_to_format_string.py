#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def get_format_string(pattern: re.Pattern | str) -> str:
    if isinstance(pattern, re.Pattern):
        pattern = pattern.pattern

    pattern = pattern.strip("^$")
    return re.sub(r"\(.+?\)", "{}", pattern)


if __name__ == "__main__":
    PATTERN_BOOK = re.compile(r"^book_([a-fA-F\d]+)$")
    fmt = get_format_string(PATTERN_BOOK)
    print(fmt)
    assert fmt == "book_{}"

    PATTERN_BOOK_IMAGE = re.compile(r"^([a-fA-F\d]+)_image_(.+)$")
    fmt = get_format_string(PATTERN_BOOK_IMAGE)
    print(fmt)
    assert fmt == "{}_image_{}"

    PATTERN_BOOK_ANNOTATION = re.compile(r"^([a-fA-F\d]+)_annotation$")
    fmt = get_format_string(PATTERN_BOOK_ANNOTATION)
    print(fmt)
    assert fmt == "{}_annotation"

    PATTERN_HIDE_IMAGE = "hide_image"
    fmt = get_format_string(PATTERN_HIDE_IMAGE)
    print(fmt)
    assert fmt == "hide_image"
