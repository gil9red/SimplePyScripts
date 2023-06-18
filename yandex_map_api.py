#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


api_key = None
url = "https://search-maps.yandex.ru/v1/?text=Магнитогорск, бизнец-центра&type=biz&lang=ru_RU&apikey={}".format(
    api_key
)
print(requests.get(url).json())
