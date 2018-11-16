#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import get_client

qb = get_client()
print('Get qBittorrent version:', qb.qbittorrent_version)
print('Get WEB API version:', qb.api_version)
print('Get minimum WEB API version:', qb.api_min_version)
