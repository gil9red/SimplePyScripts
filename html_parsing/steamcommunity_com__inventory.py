#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests


url = 'https://steamcommunity.com/inventory/76561198881890346/440/2?l=russian&count=75'

rs = requests.get(url)
data = rs.json()
assets = data['assets']

id_by_item = {
    item['instanceid']: item
    for item in data['descriptions']
}

for asset in assets:
    app_id = asset['appid']
    context_id = asset['contextid']
    asset_id = asset['assetid']
    instance_id = asset['instanceid']

    item_name = id_by_item[instance_id]['name'].strip()
    print(f'ID: {app_id}_{context_id}_{asset_id}. Name: {item_name}')

"""
ID: 440_2_9980235616. Name: Наёмник
ID: 440_2_9980256674. Name: Кепка Манн Ко
"""
