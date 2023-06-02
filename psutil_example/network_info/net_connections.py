#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil

# pip install tabulate
from tabulate import tabulate


net_connections = psutil.net_connections()
print(f"Net connections ({len(net_connections)}):")

# Sort by pid
net_connections.sort(key=lambda x: x.pid)

# for connect in net_connections:
#     print(connect)
# #
# # OR:
# #
if net_connections:
    headers = net_connections[0]._fields
    headers = [header.upper() for header in headers]

    rows = [tuple(info) for info in net_connections]
    print(tabulate(rows, headers=headers, tablefmt="grid", showindex=True))
