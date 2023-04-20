#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


net_interface_by_address_list = list(psutil.net_if_addrs().items())
print(f"Net interface by address list ({len(net_interface_by_address_list)}):")

# Sort by name interface
net_interface_by_address_list.sort(key=lambda x: x[0])

# for name, address_list in net_interface_by_address_list:
#     print(name)
#     for x in address_list:
#         print('   ', x)
#
#     print()
# #
# # OR:
# #
if net_interface_by_address_list:
    headers = ("name",) + net_interface_by_address_list[0][1][0]._fields
    headers = [header.upper() for header in headers]

    rows = []

    for name, address_list in net_interface_by_address_list:
        for i, address in enumerate(address_list):
            rows.append((name if i == 0 else "",) + tuple(address))

    # pip install tabulate
    from tabulate import tabulate
    print(tabulate(rows, headers=headers, tablefmt="grid"))
