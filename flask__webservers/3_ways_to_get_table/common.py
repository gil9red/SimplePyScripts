#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def generate_table(size=20) -> list[list[str]]:
    items = [[str(i) for i in range(size + 1)]]

    for i in range(1, size + 1):
        row = [str(i)]

        for j in range(1, size + 1):
            row.append(str(i * j))

        items.append(row)

    items[0][0] = ""

    return items


if __name__ == "__main__":
    print(generate_table(5))
    print(generate_table(2))

    assert generate_table(2) == [["", "1", "2"], ["1", "1", "2"], ["2", "2", "4"]]
