#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт выводит список ip государственных организаций.

"""


import ipaddress
import sys

import requests


rs = requests.get(
    "https://jarib.github.io/anon-history/RuGovEdits/ru/latest/ranges.json"
)

# Проверка удачного запроса и полученных данных
if not rs or not rs.json() or "ranges" not in rs.json():
    print("Не получилось получить список ip государственных организаций")
    sys.exit()

# Получение и сортировка элементов по названию организации
items = sorted(rs.json()["ranges"].items(), key=lambda x: x[0])

ip_counter = 0

for i, (name, ip_network_list) in enumerate(items, 1):
    print(f"{i}. {name}")

    # Получение ip с маской подсети
    for ip_network in ip_network_list:
        print(f"    {ip_network}:")

        # Получение ip подсети
        net4 = ipaddress.ip_network(ip_network)

        # Перебор ip адресов указанной организации
        for ip in net4.hosts():
            print(f"        {ip}")
            ip_counter += 1

print()
print("Всего ip:", ip_counter)
