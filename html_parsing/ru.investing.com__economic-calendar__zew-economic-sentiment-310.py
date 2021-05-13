#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


def get_text(node) -> str:
    return node.get_text(strip=True) if node else ''


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
}

rs = requests.get('https://ru.investing.com/economic-calendar/zew-economic-sentiment-310', headers=headers)
root = BeautifulSoup(rs.content, 'html.parser')

for tr in root.select('#eventHistoryTable310 > tbody > tr'):
    tds = tr.select('td')
    td_date, td_time, td_fact, td_prog, td_pred, _ = tds
    print(get_text(td_date), get_text(td_time), get_text(td_fact), get_text(td_prog), get_text(td_pred))

"""
11.05.2021 (май) 12:00 84,0  66,3
13.04.2021 (апр) 12:00 66,3  74,0
16.03.2021 (мар) 13:00 74,0  69,6
16.02.2021 (фев) 13:00 69,6  58,3
19.01.2021 (янв) 13:00 58,3  54,4
08.12.2020 (дек) 13:00 54,4 37,5 32,8
"""
