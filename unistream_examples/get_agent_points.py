#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Получение перечня точек предоставления услуг партнера.

Получение перечня дочерних узлов партнера. Если признак получения всех потомков установлен, то будут возвращены
все точки предоставления услуг партнера с указанным идентификатором. В противном случае будут возвращены только
дети указанного партнера.

GET https://test.api.unistream.com/v1/agents/{agentId}/poses?plainlist={plainlist}
"""


import requests

from utils import get_today_RFC1123_date, get_authorization_header
from config import APPLICATION_ID, SECRET


# Идентификатор партнера
AGENT_ID = -1

# Признак получения всех потомков
PLAINLIST = False

URL = f"https://test.api.unistream.com/v1/agents/{AGENT_ID}/poses?plainlist={PLAINLIST}"

TODAY_DATE = get_today_RFC1123_date()

headers = dict()
headers["Date"] = TODAY_DATE
headers["Authorization"] = get_authorization_header(
    APPLICATION_ID, SECRET, TODAY_DATE, URL, headers
)

rs = requests.get(URL, headers=headers)
print(rs)
print(rs.text)
