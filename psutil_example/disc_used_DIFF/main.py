#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install tabulate
from tabulate import tabulate

from common import get_disc_list, get_disc_used, get_human_sizes, get_row_for, load_snapshot_raw_disc_used


disc_list = get_disc_list()
disc_list_raw = get_disc_used(disc_list, only_raw=True)

disc_list_snapshot_raw = load_snapshot_raw_disc_used()
disc_list_diff_raw = [b-a for a, b in zip(disc_list_snapshot_raw, disc_list_raw)]

headers = [''] + disc_list + ['TOTAL USED']
rows = [
    get_row_for('<SNAPSHOT>', disc_list_snapshot_raw),
    get_row_for('<CURRENT>', disc_list_raw),
    get_row_for('<DIFF>', disc_list_diff_raw, with_sign=True),
]

print()
print(tabulate(rows, headers=headers, tablefmt="grid"))
