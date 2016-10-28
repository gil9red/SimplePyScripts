#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    from datetime import date
    date_req1 = '01.01.2000'
    date_req2 = date.today().strftime('%d.%m.%Y')

    file_name = 'metall_{}-{}.xml'.format(date_req1, date_req2)

    # Кеширование. Если файла нет, то скачиваем его.
    import os.path
    if not os.path.exists(file_name):
        url = 'http://www.cbr.ru/scripts/xml_metall.asp?date_req1={}&date_req2={}'.format(date_req1, date_req2)

        with open(file_name, 'w') as f:
            import requests
            rs = requests.get(url)
            f.write(rs.text)

    with open(file_name, 'rb') as f:
        from bs4 import BeautifulSoup
        root = BeautifulSoup(f, "xml")

        # Code="1" -- Золото
        # Code="2" -- Серебро
        # Code="3" -- Платина
        # Code="4" -- Палладий
        records = root.find_all('Record', attrs=dict(Code="1"))

        # for i, record in enumerate((records[0], records[-1]), 1):
        for i, record in enumerate(records, 1):
            # b'<Record Date="06.01.2000" Code="1"><Buy>231,94</Buy><Sell>246,67</Sell></Record>\n\n'
            # record["Code"]
            print('{}. {}: {}'.format(i, record["Date"], record.findChild("Buy").text))
