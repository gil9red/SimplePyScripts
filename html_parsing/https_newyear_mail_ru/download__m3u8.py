#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


rs = requests.get("https://newyear.mail.ru/video/man/kolya/sweets/manifest.m3u8")
print(rs.content)

rs = requests.get("https://newyear.mail.ru/video/man/kolya/games/manifest.m3u8")
print(rs.content)
