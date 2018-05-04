#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
rs = requests.get('http://jsonip.com/')
print(rs.json()['ip'])

# OR:
# from urllib.request import urlopen
# import json
#
# with urlopen('http://jsonip.com/') as f:
#     print(json.loads(f.read())['ip'])
