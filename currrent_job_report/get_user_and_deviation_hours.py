#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import datetime as DT
import os.path
import re

from lxml import etree

import requests
requests.packages.urllib3.disable_warnings()


class NotFoundReport(Exception):
    pass


URL = 'https://jira.compassplus.ru/pa-reports/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'

# NOTE: Get <PEM_FILE_NAME>: openssl pkcs12 -nodes -out key.pem -in file.p12
PEM_FILE_NAME = os.path.abspath('ipetrash.pem')


def clear_hours(hours: str) -> str:
    return re.sub(r'[^\d:-]', '', hours)


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/4e4efd7467795aa5881c8b22a5829314ba71f409/get_quarter.py#L10
def get_quarter(month_or_date=None) -> int:
    dt = month_or_date
    if dt is None:
        dt = DT.date.today()

    if isinstance(dt, int):
        month = dt
    else:
        month = dt.month

    if month in (1, 2, 3):
        return 1

    elif month in (4, 5, 6):
        return 2

    elif month in (7, 8, 9):
        return 3

    elif month in (10, 11, 12):
        return 4

    else:
        raise Exception('Invalid "month": {}'.format(month))


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/21102725da9b024ce17ab0a78d6a8d14858db146/get_quarter.py#L36
def get_quarter_num(month_or_date=None) -> str:
    return ['I', 'II', 'III', 'IV'][get_quarter(month_or_date) - 1]


def _send_data(data: dict) -> str:
    headers = {
        'User-Agent': USER_AGENT,
    }

    rs = requests.post(URL, data=data, headers=headers, cert=PEM_FILE_NAME, verify=False)
    if not rs.ok:
        raise NotFoundReport('HTTP status is {}'.format(rs.status_code))

    return rs.text


def get_report_context() -> str:
    today = DT.datetime.today()
    data = {
        'dep': 'dep4',
        'rep': 'rep1',
        'period': today.strftime('%Y-%m'),
        'v': int(today.timestamp() * 1000),
        'type': 'normal',
    }
    return _send_data(data)


def get_quarter_report_context() -> str:
    today = DT.datetime.today()
    data = {
        'dep': 'dep12',
        'rep': 'rep1',
        'quarter': 'quarter',
        'period': f'{today.year}-q{get_quarter(today)}',
        'v': int(today.timestamp() * 1000),
        'type': 'normal',
    }
    return _send_data(data)


def parse_current_user_deviation_hours(html: str) -> (str, str):
    root = etree.HTML(html)

    XPATH_1 = '//table[@id="report"]/tbody/tr[th[contains(text(),"Текущий пользователь")]]'
    XPATH_2 = '//table[@class="report"]/tbody/tr[th[contains(text(),"Текущий пользователь")]]'

    # Вытаскивание tr, у которого есть вложенный th, имеющий в содержимом текст "Текущий пользователь"
    try:
        items = root.xpath(XPATH_1)
        if not items:
            items = root.xpath(XPATH_2)

        current_user_tr = items[0]

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
    return name, clear_hours(deviation_hours)


def parse_user_deviation_hours(html: str, user_name: str = 'Петраш') -> (str, str):
    root = etree.HTML(html)

    XPATH_1 = f'//table[@id="report"]/tbody/tr[td[contains(text(),"{user_name}")]]'
    XPATH_2 = f'//table[@class="report"]/tbody/tr[td[contains(text(),"{user_name}")]]'

    # Вытаскивание tr, у которого есть вложенный th, имеющий в содержимом текст "Текущий пользователь"
    try:
        items = root.xpath(XPATH_1)
        if not items:
            items = root.xpath(XPATH_2)

        current_user_tr = items[0]

    except IndexError:
        raise NotFoundReport()

    # Получение текста текущего элемента
    name = next(current_user_tr.iterchildren()).text.strip()

    # Получение следующего следующего элемента после текущего, у него получение последнего
    # ребенка, у которого вытаскивается текст
    # Ищем последную строку текущего пользователя -- в ней и находится время работы
    # Ее легко найти -- ее первая ячейка пустая
    deviation_tr = current_user_tr.getnext()

    # Ищем строку с пустой ячейкой
    while next(deviation_tr.iterchildren()).text.strip():
        deviation_tr = deviation_tr.getnext()

    deviation_hours = deviation_tr.getchildren()[-1].text.strip()
    return name, clear_hours(deviation_hours)


def get_user_and_deviation_hours() -> (str, str):
    content = get_report_context()
    return parse_current_user_deviation_hours(content)


def get_quarter_user_and_deviation_hours() -> (str, str):
    content = get_quarter_report_context()
    return parse_user_deviation_hours(content)


if __name__ == '__main__':
    name, deviation_hours = get_user_and_deviation_hours()
    print(name)
    print(('Недоработка' if deviation_hours[0] == '-' else 'Переработка') + ' ' + deviation_hours)
    print()

    name, deviation_hours = get_quarter_user_and_deviation_hours()
    print(name)
    print(('Недоработка' if deviation_hours[0] == '-' else 'Переработка') + ' за квартал ' + deviation_hours)
