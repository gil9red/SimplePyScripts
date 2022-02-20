#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import decimal
import enum
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag


class MetalEnum(enum.IntEnum):
    Gold = 1
    Silver = 2
    Platinum = 3
    Palladium = 4


@dataclass
class MetalRate:
    date: DT.date
    code: MetalEnum
    amount: decimal.Decimal

    @classmethod
    def parse_from_xml(cls, tag: Tag) -> 'MetalRate':
        date = DT.datetime.strptime(tag['date'], '%d.%m.%Y').date()
        code = int(tag['code'])
        amount = decimal.Decimal(tag.sell.text.replace(',', '.'))

        return cls(date, MetalEnum(code), amount)


decimal.getcontext().prec = 2


def get_next_date(date: DT.date) -> DT.date:
    return (date + DT.timedelta(days=31)).replace(day=1)


def get_date_str(date: DT.date) -> str:
    return date.strftime('%d/%m/%Y')


# TODO: ...
START_DATE_REQ1 = DT.date(year=2000, month=1, day=1)

# TODO: db.py

# TODO: нужен код, который возьмет последнюю загруженную дату и составит список пар date_req1 и date_req2 по месяцам
#       т.е. из api всегда берем только за 1 месяц

date_req1 = DT.date.today().replace(day=1)
date_req2 = get_next_date(date_req1)

params = {
    'date_req1': get_date_str(date_req1),
    'date_req2': get_date_str(date_req2),
}
rs = requests.get('http://www.cbr.ru/scripts/xml_metall.asp', params=params)
print(rs)
rs.raise_for_status()

root = BeautifulSoup(rs.content, 'html.parser')
metal_rates = [
    MetalRate.parse_from_xml(r)
    for r in root.select('Record')
]
print(*metal_rates, sep='\n')
