#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
from decimal import Decimal


data = (
    (
        69695,
        "CASTROL",
        "156f9d",
        "Castrol EDGE Professional A5 5W30 (1л) Lаnd Rover",
        "Castrol-156F9D-Castrol EDGE Professional A5 5W30 (1л) Lаnd Rover",
        Decimal("1.00"),
        "",
        Decimal("684.25"),
        0,
        13155264,
        "",
        Decimal("0.00"),
        Decimal("0.00"),
        Decimal("0.00"),
        Decimal("0.00"),
        Decimal("0.00"),
        "7",
        "",
        "",
    ),
    (
        69695,
        "CASTROL",
        "15667c",
        "Castrol EDGE Titanium 5W30 LL 504.00/507.00 (1L).Масло моторное",
        "Castrol-15667C-Castrol EDGE Titanium 5W30 LL 504.00/507.00 (1L).Масло моторное",
        Decimal("40.00"),
        "",
        Decimal("599.15"),
        0,
        13155265,
        "",
        Decimal("0.00"),
        Decimal("0.00"),
        Decimal("0.00"),
        Decimal("0.00"),
        Decimal("0.00"),
        "7",
        "",
        "",
    ),
)
print(data)


def my_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)

    # Далее можно описывать и другие свои типы, например MyFooFooBar
    # elif isinstance(obj, MyFooFooBar):
    #     return obj.get_super_foo_bar_value()

    # Если не удалось определить тип:
    return str(obj)


json_data = json.dumps(data, ensure_ascii=False, default=str)
print(json_data)

json_data = json.dumps(data, ensure_ascii=False, default=my_default)
print(json_data)
