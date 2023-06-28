#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Получение деталей.

GET https://test.api.unistream.com/v1/operations/{id}/details.
"""


import requests

from utils import get_today_RFC1123_date, get_authorization_header
from config import APPLICATION_ID, SECRET, UNISTREAM_BANK_ID


OPERATION_GUID = "<OPERATION_GUID>"
URL = f"https://test.api.unistream.com/v1/operations/{OPERATION_GUID}/details"
TODAY_DATE = get_today_RFC1123_date()

headers = dict()
headers["Date"] = TODAY_DATE
headers["X-Unistream-Security-PosId"] = UNISTREAM_BANK_ID
headers["Authorization"] = get_authorization_header(
    APPLICATION_ID, SECRET, TODAY_DATE, URL, headers
)

rs = requests.get(URL, headers=headers)
print(rs)
print(rs.text)
