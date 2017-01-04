#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт выводит список ip государственных организаций.

"""


if __name__ == '__main__':
    import requests
    rs = requests.get('https://jarib.github.io/anon-history/RuGovEdits/ru/latest/ranges.json')

    # Проверка удачного запроса и полученных данных
    if not rs or not rs.json() or 'ranges' not in rs.json():
        print('Не получилось получить список ip государственных организаций')
        quit()

    # Получение и сортировка элементов по названию организации
    items = sorted(rs.json()['ranges'].items(), key=lambda x: x[0])

    ip_counter = 0

    for i, (name, ip_network_list) in enumerate(items, 1):
        print('{}. {}'.format(i, name))

        # Получени ip с маской подсети
        for ip_network in ip_network_list:
            print('    {}:'.format(ip_network))

            # Получение ip подсети
            import ipaddress
            net4 = ipaddress.ip_network(ip_network)

            # Перебор ip адресов указанной организации
            for ip in net4.hosts():
                print('        {}'.format(ip))
                ip_counter += 1

    print()
    print('Всего ip:', ip_counter)