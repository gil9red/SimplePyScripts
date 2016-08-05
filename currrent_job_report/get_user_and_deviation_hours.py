#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime

import requests
requests.packages.urllib3.disable_warnings()

URL = 'https://confluence.compassplus.ru/reports/index.jsp'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'

import os.path
PEM_FILE_NAME = 'ipetrash.pem'
PEM_FILE_NAME = os.path.join(os.path.dirname(__file__), PEM_FILE_NAME)


def get_report_context():
    today = datetime.today()
    data = {
        'dep': 'all',
        'rep': 'rep1',
        'period': today.strftime('%Y-%m'),
        'v': int(today.timestamp() * 1000),
        'type': 'normal',
    }

    headers = {
        'User-Agent': USER_AGENT,
    }

    rs = requests.post(URL, data=data, headers=headers, cert=PEM_FILE_NAME, verify=False)
    return rs.text


def get_user_and_deviation_hours():
    content = get_report_context()

    from lxml import etree
    root = etree.HTML(content)
    # Вытаскивание tr, у которого есть вложенный th, имеющий в содержимом текст "Текущий пользователь"
    current_user_tr = root.xpath('//table[@id="report"]/tbody/tr[th[contains(text(),"Текущий пользователь")]]')[0]

    # Получение следующего элемента после текущего, у него получение первого ребенка, у которого вытаскивается текст
    name = next(current_user_tr.getnext().iterchildren()).text.strip()

    # Получение следующего следующего элемента после текущего, у него получение последнего
    # ребенка, у которого вытаскивается текст
    deviation_hours = current_user_tr.getnext().getnext().getchildren()[-1].text.strip()

    return name, deviation_hours


if __name__ == '__main__':
    name, deviation_hours = get_user_and_deviation_hours()
    print(name)
    print(('Недоработка' if deviation_hours[0] == '-' else 'Переработка') + ' ' + deviation_hours)
