#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
from typing import List, Dict
from pathlib import Path

# pip install tabulate
from tabulate import tabulate

# pip install python-qbittorrent
from qbittorrent import Client

from config import IP_HOST, USER, PASSWORD

sys.path.append(str(Path(__file__).resolve().parent.parent))
from human_byte_size import sizeof_fmt


def print_table(rows: List[List[str]], headers: List[str], show_index=True):
    if show_index:
        show_index = range(1, len(rows) + 1)

    text = tabulate(rows, headers=headers, tablefmt="grid", showindex=show_index)
    print(text)


def print_files_table(files: List[Dict]):
    rows = [(file['name'], sizeof_fmt(file['size'])) for file in sorted(files, key=lambda x: x['name'])]
    headers = ['#', 'File Name', 'Size']
    print_table(rows, headers)


def print_torrents(torrents: List[Dict]):
    total_size = 0

    for i, torrent in enumerate(torrents, 1):
        torrent_size = torrent['total_size']
        total_size += torrent_size

        print(f"{i:3}. {torrent['name']} ({sizeof_fmt(torrent_size)})")

    print()
    print(f'Total torrents: {len(torrents)}, total size: {sizeof_fmt(total_size)} ({total_size} bytes)')


def get_client() -> Client:
    client = Client(IP_HOST)
    client.login(USER, PASSWORD)
    return client
