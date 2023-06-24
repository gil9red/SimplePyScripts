#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/910435/201445


def convert(name: str) -> str:
    parts = name.split()
    return parts[0] + " " + "".join(x[0] + "." for x in parts[1:])


if __name__ == "__main__":
    authors = ["Иванов Иван", "Петров Петр Петрович"]
    items = [convert(x) for x in authors]
    print(items)  # ["Иванов И.", "Петров П.П."]
