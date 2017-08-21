#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install psutil
import psutil

# pip install tabulate
from tabulate import tabulate

net_interface_list = list(psutil.net_io_counters(pernic=True).items())
print('Net interface list ({}):'.format(len(net_interface_list)))

# Sort by name interface
net_interface_list.sort(key=lambda x: x[0])

# for interface, info in net_interface_list:
#     print('"{}": {}'.format(interface, info))
# #
# # OR:
# #
if net_interface_list:
    info_fields = net_interface_list[0][1]._fields
    headers = ('name',) + info_fields
    headers = [header.upper() for header in headers]

    rows = [(interface,) + tuple(info) for interface, info in net_interface_list]

    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print()
    print()

net_connections = psutil.net_connections()
print('Net connections ({}):'.format(len(net_connections)))

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
    print()
    print()

net_interface_by_address_list = list(psutil.net_if_addrs().items())
print('Net interface by address list ({}):'.format(len(net_interface_by_address_list)))

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
    headers = ('name',) + net_interface_by_address_list[0][1][0]._fields
    headers = [header.upper() for header in headers]

    rows = []

    for name, address_list in net_interface_by_address_list:
        for i, address in enumerate(address_list):
            rows.append((name if i == 0 else '',) + tuple(address))

    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print()
    print()

network_interface_card_by_info = list(psutil.net_if_stats().items())
print('Network interface card by info ({}):'.format(len(network_interface_card_by_info)))

# Sort by name interface
network_interface_card_by_info.sort(key=lambda x: x[0])

# for name, info in network_interface_card_by_info:
#     print(name, info)
# #
# # OR:
# #

if network_interface_card_by_info:
    headers = ('name',) + network_interface_card_by_info[0][1]._fields
    headers = [header.upper() for header in headers]

    rows = [(name,) + tuple(info) for name, info in network_interface_card_by_info]

    print(tabulate(rows, headers=headers, tablefmt="grid"))
    print()
    print()
