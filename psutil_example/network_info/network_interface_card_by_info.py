#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


network_interface_card_by_info = list(psutil.net_if_stats().items())
print(f"Network interface card by info ({len(network_interface_card_by_info)}):")

# Sort by name interface
network_interface_card_by_info.sort(key=lambda x: x[0])

# for name, info in network_interface_card_by_info:
#     print(name, info)
# #
# # OR:
# #

if network_interface_card_by_info:
    headers = ("name",) + network_interface_card_by_info[0][1]._fields
    headers = [header.upper() for header in headers]

    rows = [(name,) + tuple(info) for name, info in network_interface_card_by_info]

    # pip install tabulate
    from tabulate import tabulate
    print(tabulate(rows, headers=headers, tablefmt="grid"))
