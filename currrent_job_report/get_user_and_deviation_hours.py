#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime

import requests
requests.packages.urllib3.disable_warnings()

URL = 'https://confluence.compassplus.ru/reports/index.jsp'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'

import os.path
PEM_FILE_NAME = os.path.abspath('ipetrash.pem')


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


class NotFoundReport(Exception):
    pass


def get_user_and_deviation_hours():
    content = get_report_context()

    from lxml import etree
    root = etree.HTML(content)

    try:
        # Вытаскивание tr, у которого есть вложенный th, имеющий в содержимом текст "Текущий пользователь"
        current_user_tr = root.xpath('//table[@id="report"]/tbody/tr[th[contains(text(),"Текущий пользователь")]]')[0]
    except IndexError:
        raise NotFoundReport()

    # Получение следующего элемента после текущего, у него получение первого ребенка, у которого вытаскивается текст
    name = next(current_user_tr.getnext().iterchildren()).text.strip()

    # Получение следующего следующего элемента после текущего, у него получение последнего
    # ребенка, у которого вытаскивается текст
    # Ищем последную строку текущего пользователя -- в ней и находится время работы
    # Ее легко найти -- ее первая ячейка пустая
    deviation_tr = current_user_tr.getnext()

    # Ищем строку с пустой ячейкой
    while next(deviation_tr.iterchildren()).text.strip():
        deviation_tr = deviation_tr.getnext()

    deviation_hours = deviation_tr.getchildren()[-1].text.strip()

    return name, deviation_hours


if __name__ == '__main__':
    name, deviation_hours = get_user_and_deviation_hours()
    print(name)
    print(('Недоработка' if deviation_hours[0] == '-' else 'Переработка') + ' ' + deviation_hours)
