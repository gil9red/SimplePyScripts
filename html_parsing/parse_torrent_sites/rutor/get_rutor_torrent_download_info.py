#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

import requests
from bs4 import BeautifulSoup


def get_rutor_torrent_download_info(torrent_url):
    """
    Parse torrent url and return tuple: (torrent_file_url, magnet_url, info_hash)

    """

    rs = requests.get(torrent_url)
    root = BeautifulSoup(rs.content, "lxml")

    magnet_url = root.select_one('#download > a[href^="magnet"]')["href"]

    # For get info hash from magnet url
    match = re.compile(r"btih:([abcdef\d]+?)&", flags=re.IGNORECASE).search(magnet_url)
    if match:
        info_hash = match.group(1)

    return torrent_url.replace("/torrent/", "/download/"), magnet_url, info_hash


if __name__ == "__main__":
    torrent_url = "http://anti-tor.org/torrent/544942"
    torrent_file_url, magnet_url, info_hash = get_rutor_torrent_download_info(
        torrent_url
    )
    print(torrent_file_url)
    print(magnet_url)
    print(info_hash)
