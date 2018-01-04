#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install python-qbittorrent
from qbittorrent import Client
from config import IP_HOST, USER, PASSWORD

qb = Client(IP_HOST)
qb.login(USER, PASSWORD)

print('Get qBittorrent version:', qb.qbittorrent_version)
print('Get WEB API version:', qb.api_version)
print('Get minimum WEB API version:', qb.api_min_version)
