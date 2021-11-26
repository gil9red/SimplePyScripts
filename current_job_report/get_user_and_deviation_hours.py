#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


import datetime as DT
import re
import sys
import ssl

from pathlib import Path
from typing import Tuple

import requests
requests.packages.urllib3.disable_warnings()

from lxml import etree


DIR = Path(__file__).resolve().parent

sys.path.append(str(DIR.parent))
from get_quarter import get_quarter, get_quarter_num


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


class NotFoundReport(Exception):
    pass


URL = 'https://jira.compassplus.ru/pa-reports/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'

# NOTE: Get <PEM_FILE_NAME>: openssl pkcs12 -nodes -out ipetrash.pem -in ipetrash.p12
PEM_FILE_NAME = str(DIR / 'ipetrash.pem')


session = requests.session()
session.cert = PEM_FILE_NAME
session.mount('https://', TLSAdapter())
session.headers['User-Agent'] = USER_AGENT


def clear_hours(hours: str) -> str:
    return re.sub(r'[^\d:-]', '', hours)


def _send_data(data: dict) -> str:
    rs = session.post(URL, data=data)
    if not rs.ok:
        raise NotFoundReport(f"HTTP status is {rs.status_code}")

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


def parse_current_user_deviation_hours(html: str) -> Tuple[str, str]:
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


def parse_user_deviation_hours(html: str, user_name: str = 'Петраш') -> Tuple[str, str]:
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


def get_user_and_deviation_hours() -> Tuple[str, str]:
    content = get_report_context()
    return parse_current_user_deviation_hours(content)


def get_quarter_user_and_deviation_hours() -> Tuple[str, str]:
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
