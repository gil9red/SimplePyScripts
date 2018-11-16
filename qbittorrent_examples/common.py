#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install tabulate
from tabulate import tabulate

# pip install python-qbittorrent
from qbittorrent import Client
from config import IP_HOST, USER, PASSWORD


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


def print_table(rows, headers, show_index=True):
    if show_index:
        show_index = range(1, len(rows) + 1)

    text = tabulate(rows, headers=headers, tablefmt="grid", showindex=show_index)
    print(text)


def print_files_table(files):
    rows = [(file['name'], sizeof_fmt(file['size'])) for file in sorted(files, key=lambda x: x['name'])]
    headers = ['#', 'File Name', 'Size']
    print_table(rows, headers)


def get_client() -> Client:
    client = Client(IP_HOST)
    client.login(USER, PASSWORD)
    return client
