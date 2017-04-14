#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


api_key = None
url = 'https://search-maps.yandex.ru/v1/?text=Магнитогорск, бизнец-центра&type=biz&lang=ru_RU&apikey={}'.format(api_key)
import requests
print(requests.get(url).json())
