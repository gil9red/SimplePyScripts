#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import requests


GET_MINIMAL_TORRENT_URL = re.compile(r"(https?://.+/torrent/\d+/?)")


def download_torrent_file(torrent_file_url):
    """
    Функция скачает по ссылке торрент файл и вернет его название.
    Если не получится, вернет None

    """

    user_agent = (
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    )

    rs = requests.get(torrent_file_url, headers={"User-Agent": user_agent})
    if not rs.ok:
        print("Не получилось скачать: {}\n\n{}".format(rs.status_code, rs.text))
        return

    # Теперь нужно вытащить название торрент-файла
    file_name = rs.headers["Content-Disposition"]
    file_name = file_name.replace("attachment; filename=", "").replace('"', "")

    with open(file_name, "wb") as f:
        f.write(rs.text.encode())

        return file_name


def get_download_url_from_torrent_url(torrent_url):
    """
    Функция по ссылке на торрент вернет ссылку на торрент-файл.
    Если не получится, вернется None.

    """

    match = GET_MINIMAL_TORRENT_URL.search(torrent_url)
    if match:
        torrent_url = match.group(1)
        download_torrent_url = torrent_url.replace("/torrent/", "/download/")
        return download_torrent_url


if __name__ == "__main__":
    torrent_url = "http://anti-tor.org/torrent/539888/7-days-to-die-v-15.1-2013-pc-repack-ot-pioneer"
    torrent_file_url = get_download_url_from_torrent_url(torrent_url)
    file_name = download_torrent_file(torrent_file_url)
    print(torrent_file_url, file_name)

    torrent_url = "http://anti-tor.org/torrent/474477/hyperdimension-neptunia-rebirth2-sisters-generation-2015-pc-repack-ot-r.g-games"
    torrent_file_url = get_download_url_from_torrent_url(torrent_url)
    file_name = download_torrent_file(torrent_file_url)
    print(torrent_file_url, file_name)

    torrent_url = "http://anti-tor.org/torrent/543446/the-binding-of-isaac-rebirth-complete-bundle-v.1.??-2014-pc-steam-rip-ot-letsrlay"
    torrent_file_url = get_download_url_from_torrent_url(torrent_url)
    file_name = download_torrent_file(torrent_file_url)
    print(torrent_file_url, file_name)
