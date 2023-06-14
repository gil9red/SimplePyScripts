#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def split_by_case(text: str) -> list:
    return re.findall(r"[a-zA-Z][a-z]+", text)


if __name__ == "__main__":
    print(split_by_case("fadeInLeft"))
    print(split_by_case("CharSequence"))
    print(split_by_case("String"))
    print(split_by_case("compareToIgnoreCase"))

    assert split_by_case("fadeInLeft") == ["fade", "In", "Left"]
    assert split_by_case("CharSequence") == ["Char", "Sequence"]
    assert split_by_case("String") == ["String"]
    assert split_by_case("compareToIgnoreCase") == ["compare", "To", "Ignore", "Case"]
