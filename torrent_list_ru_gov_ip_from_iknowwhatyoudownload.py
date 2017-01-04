#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт, используя сервис http://iknowwhatyoudownload.com показывает список торрентов которые были скачаны
из ip государственных организаций.
Список ip организаций скачивается из репозитория github.

"""

# NOTE: На момент написания скрипта ни один из ip не был в базе iknowwhatyoudownload


def get_torrents_by_ip(ip):
    url = 'http://iknowwhatyoudownload.com/ru/peer/?ip=' + ip

    import requests
    rs = requests.get(url, headers={'User-Agent': '-'})

    from bs4 import BeautifulSoup
    root = BeautifulSoup(rs.content, 'lxml')

    return [item.text.strip() for item in root.select('.torrent_files > a')]


if __name__ == '__main__':
    import requests
    rs = requests.get('https://jarib.github.io/anon-history/RuGovEdits/ru/latest/ranges.json')

    # Проверка удачного запроса и полученных данных
    if not rs or not rs.json() or 'ranges' not in rs.json():
        print('Не получилось получить список ip государственных организаций')
        quit()

    # Получение и сортировка элементов по названию организации
    items = sorted(rs.json()['ranges'].items(), key=lambda x: x[0])

    for i, (name, ip_list) in enumerate(items, 1):
        print('{}. {}'.format(i, name))

        for ip in ip_list:
            ip = ip.split('/')[0]
            torrents = get_torrents_by_ip(ip)

            print('    {}: {}'.format(ip, torrents))
