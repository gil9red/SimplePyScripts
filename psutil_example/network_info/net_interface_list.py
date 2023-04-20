#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil

net_interface_list = list(psutil.net_io_counters(pernic=True).items())
print("Net interface list ({}):".format(len(net_interface_list)))

# Sort by name interface
net_interface_list.sort(key=lambda x: x[0])

# for interface, info in net_interface_list:
#     print('"{}": {}'.format(interface, info))
# #
# # OR:
# #
if net_interface_list:
    info_fields = net_interface_list[0][1]._fields
    headers = ("name",) + info_fields
    headers = [header.upper() for header in headers]

    rows = [(interface,) + tuple(info) for interface, info in net_interface_list]

    # pip install tabulate
    from tabulate import tabulate
    print(tabulate(rows, headers=headers, tablefmt="grid"))
