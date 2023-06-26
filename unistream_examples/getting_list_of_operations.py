#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Получение списка операций с возможностью разбивки на страницы.

GET https://test.api.unistream.com/v1/operations?page={page}&pageSize={pageSize}&from={from}&to={to}&clientId={clientId}
"""


if __name__ == '__main__':
    from utils import get_today_RFC1123_date, get_authorization_header
    from config import APPLICATION_ID, SECRET, UNISTREAM_BANK_ID

    from collections import OrderedDict
    params = OrderedDict()
    params['page'] = 1
    params['pageSize'] = 10
    params['from'] = '2016-04-20T00:00:00'
    params['to'] = '2016-04-21T00:00:00'
    params['clientId'] = None

    # Не будем кодировать URL: в заголовок Authorization должен передаваться
    # path_and_query раскодированным, а requests достаточно умный, чтобы
    # сам кодировать заголовок, если нужно.
    # Раскодированный URL:
    # https://test.api.unistream.com/v1/operations?page=1&pageSize=10&from=2016-04-20T00:00:00&to=2016-04-21T00:00:00
    #
    # Кодированный URL:
    # https://test.api.unistream.com/v1/operations?page=1&pageSize=10&from=2016-04-20T00%3A00%3A00&to=2016-04-21T00%3A00%3A00
    #
    # Для кодирования нужно:
    # from urllib.parse import urlencode
    # URL = 'https://test.api.unistream.com/v1/operations' + '?' + urlencode(params)

    URL = 'https://test.api.unistream.com/v1/operations'
    URL += '?' + '&'.join(f'{k}={v}' for k, v in params.items())

    TODAY_DATE = get_today_RFC1123_date()

    import logging
    logging.basicConfig(level=logging.DEBUG)

    headers = dict()
    headers['Date'] = TODAY_DATE
    headers['X-Unistream-Security-PosId'] = UNISTREAM_BANK_ID
    headers['Authorization'] = get_authorization_header(APPLICATION_ID, SECRET, TODAY_DATE, URL, headers)

    import requests
    rs = requests.get(URL, headers=headers)
    print(rs)
    print(rs.text)
