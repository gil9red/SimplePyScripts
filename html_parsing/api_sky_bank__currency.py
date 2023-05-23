#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"


URL_GET_OFFICES = "https://api.sky.bank/currency/get-offices-list"
URL_RATES_BY_CODES = "https://api.sky.bank/currency/rates-by-codes"


rs = session.get(URL_GET_OFFICES)

office_id_by_name = {x["id"]: x["sname"] for x in rs.json()["response"]}
print(office_id_by_name)
# {24: '1 ФИЛИАЛ (закр)', 2: 'АТ "СКАЙ БАНК"', 25: 'Барвінківське відділення', 4: 'БАРВ.Ф.АКРБ "РЕГ_ОН-БАНК" ...

rs = session.post(URL_RATES_BY_CODES)
currency_by_rates = rs.json()["response"]
print(currency_by_rates)
# {'EUR': [{'id': 839871, 'currency_id': 4, 'unit': None, 'rate': None, 'date': '2022-01-28T00:00:00+02:00', ...

print()

for office_id, name in office_id_by_name.items():
    print(f"{name} (#{office_id}):")

    for currency_name, rates in currency_by_rates.items():
        for rate in rates:
            if rate["office_id"] == office_id:
                buy_rate = float(rate["buy_rate"]) / rate["buy_unit"]
                sell_rate = float(rate["sell_rate"]) / rate["sell_unit"]
                print(f"    {currency_name}: {buy_rate} | {sell_rate}")

    print()
"""
1 ФИЛИАЛ (закр) (#24):

АТ "СКАЙ БАНК" (#2):
    EUR: 32.2 | 32.35
    RUB: 0.362 | 0.371
    USD: 28.85 | 28.95

Барвінківське відділення (#25):

БАРВ.Ф.АКРБ "РЕГ_ОН-БАНК",М.БАРВ_НКОВЕ (#4):

Виртуальное ТОБО АТ "СКАЙ БАНК" (#29):
    EUR: 32.2 | 32.35
    RUB: 0.362 | 0.371
    USD: 28.85 | 28.95

Днепр (#22):

Київське відділення №1 (#21):
    EUR: 32.17 | 32.32
    RUB: 0.361 | 0.37
    USD: 28.82 | 28.9

Ф-Я N 1 АКРБ  "РЕГ_ОН-БАНК",ХАРК_В (#3):

Харківське відділення №1 (#6):
    EUR: 32.2 | 32.35
    RUB: 0.362 | 0.371
    USD: 28.85 | 28.95

Харківське відділення №11 (#16):

Харківське відділення №12 (#17):

Харківське відділення №13 (#18):

Харківське відділення №14 (#19):

Харківське відділення №2 (#7):
    EUR: 32.2 | 32.35
    RUB: 0.362 | 0.371
    USD: 28.85 | 28.95

Харківське відділення №3 (#8):
    EUR: 32.2 | 32.35
    RUB: 0.362 | 0.371
    USD: 28.85 | 28.95

Харківське відділення №4 (#9):
    EUR: 32.2 | 32.35
    RUB: 0.362 | 0.371
    USD: 28.85 | 28.95

Харківське відділення №5 (#10):
    EUR: 32.2 | 32.35
    RUB: 0.362 | 0.371
    USD: 28.85 | 28.95

Харківське відділення №7 (#12):

Харківське відділення №8 (#13):

Харківське головне відділення (#14):
    EUR: 32.2 | 32.35
    RUB: 0.362 | 0.371
    USD: 28.85 | 28.95

Харківське Центральне відділення (#23):
    EUR: 32.2 | 32.35
    RUB: 0.362 | 0.371
    USD: 28.85 | 28.95

ХВ N10 АТ `РЕГІОН-БАНК` (#15):

ХВ N15 АТ `РЕГІОН-БАНК` (#20):

ХВ N6 АТ `РЕГІОН-БАНК` (#11):

ХФ БАРВЕНКОВО(ЗАКР) (#26):

Чугуев филилал (Закр) (#28):

Чугуївське відділення (#27):

ЧУГУЇВ.Ф.АКРБ "РЕГ_ОН-БАНК", М.ЧУГУЇВ (#5):
"""
