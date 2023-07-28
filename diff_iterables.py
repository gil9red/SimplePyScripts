#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from typing import Iterable


@dataclass
class Result:
    added: list
    deleted: list


def diff_iterables(iterable_1: Iterable, iterable_2: Iterable) -> Result:
    return Result(
        added=[x for x in iterable_2 if x not in iterable_1],
        deleted=[x for x in iterable_1 if x not in iterable_2],
    )


if __name__ == "__main__":
    items_1 = "01234"
    items_2 = "12456"
    result = diff_iterables(items_1, items_2)
    print(result)
    assert (
        Result(
            added=["5", "6"],
            deleted=["0", "3"],
        )
        == result
    )
    # Result(added=['5', '6'], deleted=['0', '3'])

    assert (
        Result(added=[], deleted=[])
        == diff_iterables(items_1, items_1)
    )

    assert (
        Result(added=["4"], deleted=[])
        == diff_iterables("123", "1234")
    )

    assert (
        Result(added=[], deleted=["3"])
        == diff_iterables("123", "12")
    )
