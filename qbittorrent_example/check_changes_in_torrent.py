#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Script for download serial torrent by qbittorrent.
When serial torrent modify (example: append new series), script download new files.

"""


def get_rutor_torrent_download_info(torrent_url):
    """
    Parse torrent url and return tuple: (torrent_file_url, magnet_url, info_hash)

    """

    import requests
    rs = requests.get(torrent_url)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    magnet_url = root.select_one('#download > a[href^="magnet"]')['href']

    # For get info hash from magnet url
    import re
    match = re.compile(r'btih:([abcdef\d]+?)&', flags=re.IGNORECASE).search(magnet_url)
    if match:
        info_hash = match.group(1)

    return torrent_url.replace('/torrent/', '/download/'), magnet_url, info_hash


def download_and_parse_torrent_file(torrent_file_url):
    while True:
        try:
            import requests
            data = requests.get(torrent_file_url).content.decode('latin1')

            import effbot_bencode
            torrent = effbot_bencode.decode(data)
            return torrent

        except:
            import traceback
            print(traceback.format_exc())

            # Если произошла какая-то ошибка попытаемся через 30 секунд попробовать снова
            import time
            time.sleep(30)


def remove_previous_torrent_from_qbittorrent(qb, new_info_hash):
    info_hash_by_name_dict = {torrent['hash']: torrent['name'] for torrent in qb.torrents()}

    from collections import defaultdict
    name_by_info_hash_list_dict = defaultdict(list)

    for info_hash, name in info_hash_by_name_dict.items():
        name_by_info_hash_list_dict[name].append(info_hash)

    # If info_hash already in torrent list
    if new_info_hash in info_hash_by_name_dict:
        # Get torrent name
        name = info_hash_by_name_dict[new_info_hash]

        # Get torrents info hash with <name>
        info_hash_list = name_by_info_hash_list_dict[name]

        # Remove new (current) info hash
        info_hash_list.remove(new_info_hash)

        # Remove previous torrents
        if info_hash_list:
            print('Remove previous torrents: {}'.format(info_hash_list))
            qb.delete(info_hash_list)


if __name__ == '__main__':
    from config import *

    from qbittorrent import Client
    qb = Client(IP_HOST)
    qb.login(USER, PASSWORD)

    torrent_url = 'http://anti-tor.org/torrent/544942'

    last_number_files = 0

    while True:
        from datetime import datetime
        today = datetime.today()

        torrent_file_url, _, info_hash = get_rutor_torrent_download_info(torrent_url)
        print('{}: Проверка {}: {} / {}'.format(today, torrent_url, torrent_file_url, info_hash))

        torrent = download_and_parse_torrent_file(torrent_file_url)
        files = ["/".join(file["path"]) for file in torrent["info"]["files"]]

        if len(files) != last_number_files:
            print('Обнаружены изменения: {} файлов, {} фильмов: {}'.format(
                len(files),
                len(list(filter(lambda x: x.endswith('.avi'), files))),
                files
            ))
            last_number_files = len(files)

            # Say qbittorrent download torrent file
            qb.download_from_link(torrent_file_url)

            remove_previous_torrent_from_qbittorrent(qb, info_hash)

        else:
            print('Изменений нет')

        print()

        # Every 3 hours
        from datetime import timedelta
        today = datetime.today()
        timeout_date = today + timedelta(hours=3)

        while today <= timeout_date:
            def str_timedelta(td):
                mm, ss = divmod(td.seconds, 60)
                hh, mm = divmod(mm, 60)
                return "%d:%02d:%02d" % (hh, mm, ss)

            left = timeout_date - today
            left = str_timedelta(left)

            print('\r' * 50, end='')
            print('До следующего запуска осталось {}'.format(left), end='')

            import sys
            sys.stdout.flush()

            # Delay 1 seconds
            import time
            time.sleep(1)
            today = datetime.today()

        print('\r' * 50, end='')
        print('\n')
