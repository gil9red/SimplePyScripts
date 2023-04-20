#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install tabulate
from tabulate import tabulate

from common import (
    get_disc_list,
    get_disc_used,
    get_human_sizes,
    get_row_for,
    load_snapshot_raw_disc_used,
)


disc_list = get_disc_list()
disc_list_raw = get_disc_used(disc_list, only_raw=True)

disc_list_snapshot_raw = load_snapshot_raw_disc_used()
disc_list_diff_raw = [b - a for a, b in zip(disc_list_snapshot_raw, disc_list_raw)]

headers = [""] + disc_list + ["TOTAL USED"]
rows = [
    get_row_for("<SNAPSHOT>", disc_list_snapshot_raw),
    get_row_for("<CURRENT>", disc_list_raw),
    get_row_for("<DIFF>", disc_list_diff_raw, with_sign=True),
]

print()
print(tabulate(rows, headers=headers, tablefmt="grid"))

# Read snapshot: [629047848960, 3362506526720, 165107150848, 138658295808]
#
# +------------+----------+-----------+-----------+-----------+--------------+
# |            | C:\      | D:\       | E:\       | F:\       | TOTAL USED   |
# +============+==========+===========+===========+===========+==============+
# | <SNAPSHOT> | 585.8 GB | 3.1 TB    | 153.8 GB  | 129.1 GB  | 3.9 TB       |
# +------------+----------+-----------+-----------+-----------+--------------+
# | <CURRENT>  | 585.8 GB | 3.1 TB    | 153.8 GB  | 129.1 GB  | 3.9 TB       |
# +------------+----------+-----------+-----------+-----------+--------------+
# | <DIFF>     | -2.5 MB  | 0.0 bytes | 0.0 bytes | 0.0 bytes | -2.5 MB      |
# +------------+----------+-----------+-----------+-----------+--------------+
