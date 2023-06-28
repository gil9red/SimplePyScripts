#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Получение информации о точке предоставления услуги.

GET https://test.api.unistream.com/v1/agents/{agentId}/poses/{posId}
"""


import requests

from utils import get_today_RFC1123_date, get_authorization_header
from config import APPLICATION_ID, SECRET


# Идентификатор партнера
AGENT_ID = -1

# Идентификатор точки предоставления услуги
POS_ID = -1

params = {
    "agentId": AGENT_ID,
    "posId": POS_ID,
}
URL = "https://test.api.unistream.com/v1/agents/{agentId}/poses/{posId}".format(
    **params
)

TODAY_DATE = get_today_RFC1123_date()

headers = dict()
headers["Date"] = TODAY_DATE
headers["Authorization"] = get_authorization_header(
    APPLICATION_ID, SECRET, TODAY_DATE, URL, headers
)

rs = requests.get(URL, headers=headers)
print(rs)
print(rs.text)
