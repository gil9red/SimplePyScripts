#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import decimal
import enum
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

from config import START_DATE, FILE_COOKIES


decimal.getcontext().prec = 2

session = requests.session()

# NOTE: Зачем-то сайт с API добавил проверку на роботов, возможно, много запросов, а менять
#       работу сайта, добавляя API-key было сложно или много по времени
#       Example:
#       __ddgid=r6nn<...>4W; __ddg2=u5rq<...>wV9; __ddg1=gzBn<...>82mir; __ddgmark=W6X<...>owfI; __ddg5=ocM<...>tvM
if FILE_COOKIES.exists():
    try:
        cookies_text = FILE_COOKIES.read_text('utf-8')
        for x in cookies_text.split('; '):
            name, value = x.split('=', maxsplit=1)
            session.cookies.set(name, value)
    except:
        pass


class AutoName(enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class MetalEnum(AutoName):
    Gold = enum.auto()
    Silver = enum.auto()
    Platinum = enum.auto()
    Palladium = enum.auto()

    @classmethod
    def get_from(cls, code: int) -> 'MetalEnum':
        match code:
            case 1: return cls.Gold
            case 2: return cls.Silver
            case 3: return cls.Platinum
            case 4: return cls.Palladium

        raise KeyError(f'Unknown code {code}!')


@dataclass
class MetalRate:
    date: DT.date
    metal: MetalEnum
    amount: decimal.Decimal

    @classmethod
    def parse_from_xml(cls, tag: Tag) -> 'MetalRate':
        date = DT.datetime.strptime(tag['date'], '%d.%m.%Y').date()
        code = int(tag['code'])
        amount = decimal.Decimal(tag.sell.text.replace(',', '.'))

        return cls(date, MetalEnum.get_from(code), amount)


def get_next_date(date: DT.date) -> DT.date:
    return (date + DT.timedelta(days=31)).replace(day=1)


def get_date_str(date: DT.date) -> str:
    return date.strftime('%d/%m/%Y')


def get_pair_dates(start_date: DT.date, end_date: DT.date = None) -> list[tuple[DT.date, DT.date]]:
    if not end_date:
        end_date = DT.date.today()

    items = []
    date_req1 = start_date

    while True:
        date_req1 = date_req1.replace(day=1)
        date_req2 = get_next_date(date_req1)
        items.append((date_req1, date_req2))

        if date_req2 > end_date:
            break

        date_req1 = date_req2

    return items


def get_metal_rates(date_req1: DT.date, date_req2: DT.date) -> list[MetalRate]:
    params = {
        'date_req1': get_date_str(date_req1),
        'date_req2': get_date_str(date_req2),
    }
    rs = session.get('http://www.cbr.ru/scripts/xml_metall.asp', params=params)
    rs.raise_for_status()

    root = BeautifulSoup(rs.content, 'html.parser')
    return [
        MetalRate.parse_from_xml(r)
        for r in root.select('Record')
    ]


if __name__ == '__main__':
    pair_dates = get_pair_dates(START_DATE)
    date_req1_first, date_req2_first = pair_dates[0]
    date_req1_last, date_req2_last = pair_dates[-1]
    print(f'Total: {len(pair_dates)}')
    print(f'    {date_req1_first} - {date_req2_first}')
    print('    ...')
    print(f'    {date_req1_last} - {date_req2_last}')
    print()

    date_req1 = DT.date.today().replace(day=1)
    date_req2 = get_next_date(date_req1)

    metal_rates = get_metal_rates(date_req1, date_req2)
    print(f'Metal rates {date_req1} - {date_req2} ({len(metal_rates)}):')
    print(*metal_rates, sep='\n')
