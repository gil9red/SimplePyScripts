#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт через сервис http://iknowwhatyoudownload.com получает список торрентов которые были скачаны
из ip государственных организаций.
Список ip организаций скачивается из репозитория github.

"""


import ipaddress
import time
import sys

import requests
from bs4 import BeautifulSoup


def get_torrents_by_ip(ip, append_torrent_size=False):
    url = 'http://iknowwhatyoudownload.com/ru/peer/?ip=' + ip

    rs = requests.get(url, headers={'User-Agent': '-'})
    root = BeautifulSoup(rs.content, 'lxml')

    # Если нужно вместе с названием передавать и размер торрента
    if not append_torrent_size:
        return [item.text.strip() for item in root.select('.torrent_files > a')]

    items = []
    for row in root.select('table > tbody > tr'):
        name = row.select_one('.name-column').text.strip()
        size = row.select_one('.size-column').text.strip()

        items.append((name, size))

    return items


if __name__ == '__main__':
    rs = requests.get('https://jarib.github.io/anon-history/RuGovEdits/ru/latest/ranges.json')

    # Проверка удачного запроса и полученных данных
    if not rs or not rs.json() or 'ranges' not in rs.json():
        print('Не получилось получить список ip государственных организаций')
        sys.exit()

    # Получение и сортировка элементов по названию организации
    items = sorted(rs.json()['ranges'].items(), key=lambda x: x[0])

    for i, (name, ip_network_list) in enumerate(items, 1):
        print(f'{i}. {name}')

        # Получение ip с маской подсети
        for ip_network in ip_network_list:
            print(f'    {ip_network}:')

            # Получение ip подсети
            net4 = ipaddress.ip_network(ip_network)

            # Перебор ip адресов указанной организации
            for ip in net4.hosts():
                ip = str(ip)

                torrents = get_torrents_by_ip(ip, append_torrent_size=True)
                if torrents:
                    print(f'        {ip}. Найдено {len(torrents)}: {torrents}')

                time.sleep(0.3)
