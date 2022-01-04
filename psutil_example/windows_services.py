#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install psutil
import psutil

win_service_list = list(psutil.win_service_iter())
print(f'Win service list ({len(win_service_list)}):')

win_service_list.sort(key=lambda x: x.status())

# for win_service in win_service_list:
#     print(win_service, win_service.as_dict())
# #
# # OR:
# #
if win_service_list:
    headers = ['name', 'display_name', 'status', 'start_type', 'username', 'pid', 'binpath', 'description']

    rows = []
    for win_service in win_service_list:
        info = win_service.as_dict()
        row = [info[header] for header in headers]
        rows.append(row)

    headers = [header.upper() for header in headers]

    # pip install tabulate
    from tabulate import tabulate
    print(tabulate(rows, headers=headers, tablefmt="grid", showindex=True))
    print()

print()
name = win_service_list[0].name()
print(f'Windows service info: {name}')
win_service = psutil.win_service_get(name)
print('  win_service:', win_service)
print('  win_service info:', win_service.as_dict())
