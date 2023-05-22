#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


for i in range(20):
    url = f"https://nypromo2019.hb.bizmrg.com/video/girl-age{i}/ny2019__020.ts"
    rs = requests.get(url)
    print(i, rs)
