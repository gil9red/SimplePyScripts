#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from copy import copy
from utils import ALL_EXAMPLE_FUNC_REMOVE_DUPLICATES


ITEMS = [1, 2, 5, 3, 1, 2, 5, 7, 8]
CHECK_ITEMS = copy(ITEMS)
NEED_ITEMS = [1, 2, 3, 5, 7, 8]
print(len(ITEMS), ITEMS)
print()


for func in ALL_EXAMPLE_FUNC_REMOVE_DUPLICATES:
    print("Call:", func.__name__)

    new_items = func(ITEMS)
    assert CHECK_ITEMS == ITEMS
    assert NEED_ITEMS == sorted(new_items)

    print("    {} {}".format(len(new_items), new_items))
    print()
