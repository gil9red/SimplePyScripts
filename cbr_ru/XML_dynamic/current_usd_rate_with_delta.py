#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    # Даты: вчера и сегодня
    from datetime import date, timedelta
    date_req1 = (date.today() - timedelta(days=1)).strftime('%d/%m/%Y')
    date_req2 = date.today().strftime('%d/%m/%Y')

    # R01235 -- USD, доллары
    url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={}&date_req2={}&VAL_NM_RQ=R01235'.format(
        date_req1, date_req2
    )

    from urllib.request import urlopen
    with urlopen(url) as f:
        from bs4 import BeautifulSoup
        root = BeautifulSoup(f.read(), "xml")

        values = [float(price.text.replace(',', '.')) for price in root.select('Record > Value')]
        delta = values[1] - values[0]
        print('USD: {} ({}{:.4f})'.format(values[1], ('+' if delta > 0 else '-'), delta))
