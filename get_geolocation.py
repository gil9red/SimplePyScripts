#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
from urllib.request import urlopen


def get_geolocation() -> dict:
    location = {
        'Ip': None,
        'Country': None,

        'City': None,
        'State': None,

        'Zipcode': None,
        'Timezone': None,

        'Latitude': None,
        'Longitude': None
    }

    try:
        rs = urlopen('http://ip-api.com/json').read()
        data = json.loads(rs, encoding='utf-8')

        location['Ip'] = data['query']
        location['Country'] = data['country']

        location['City'] = data['city']
        location['State'] = data['regionName']

        location['Zipcode'] = data['zip']
        location['Timezone'] = data['timezone']

        location['Latitude'] = data['lat']
        location['Longitude'] = data['lon']

    except:
        pass

    return location


if __name__ == '__main__':
    print(get_geolocation())
