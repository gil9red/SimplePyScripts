#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Получение cписка, доступных запрашиваемой системе, партнеров

GET https://test.api.unistream.com/v1/agents
"""


import requests

from utils import get_today_RFC1123_date, get_authorization_header
from config import APPLICATION_ID, SECRET


URL = "https://test.api.unistream.com/v1/agents"
TODAY_DATE = get_today_RFC1123_date()

headers = dict()
headers["Date"] = TODAY_DATE
headers["Authorization"] = get_authorization_header(
    APPLICATION_ID, SECRET, TODAY_DATE, URL, headers
)

rs = requests.get(URL, headers=headers)
print(rs)
print(rs.text)
