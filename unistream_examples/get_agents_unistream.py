#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from utils import get_today_RFC1123_date, get_authorization_header
    from config import APPLICATION_ID, SECRET

    URL = 'https://test.api.unistream.com/v1/agents'
    TODAY_DATE = get_today_RFC1123_date()

    headers = {
        'Authorization': get_authorization_header(APPLICATION_ID, SECRET, TODAY_DATE, URL),
        'Date': TODAY_DATE,
    }

    import requests
    rs = requests.get(URL, headers=headers)
    print(rs)
    print(rs.text)
