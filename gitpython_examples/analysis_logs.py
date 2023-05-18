#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from common import return_log


if __name__ == "__main__":
    text = "\n".join(return_log(reverse=True))
    print(text)

    num_list = sorted(map(int, set(re.findall(r"Cycle commit #(\d+)", text))))
    start = num_list[0]
    end = num_list[-1]
    print(start, end)
    print()

    print(num_list)
    print(list(range(start, end + 1)))
    print()

    # Is equal?
    print(list(range(start, end + 1)) == num_list)
    print()

    # Diff
    print(set(range(start, end + 1)) - set(num_list))
    print(set(num_list) - set(range(start, end + 1)))
