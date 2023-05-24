#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


rs = requests.get("https://www.bestchange.ru/ripple-to-yoomoney.html")
root = BeautifulSoup(rs.content, "html.parser")

for tr in root.select("#content_table > tbody > tr"):
    name = tr.select_one("td.bj .pc .ca").get_text(strip=True)

    [give_el, get_el] = tr.select("td.bi")
    give = give_el.select_one(".fs").get_text(strip=True)
    get = get_el.get_text(strip=True)

    print(name, give, get, sep=" | ")

"""
ChBy | 1 XRP | 67.3091RUB ЮMoney
BtcLider | 1 XRP | 67.0861RUB ЮMoney
CryptoHome | 1 XRP | 67.0227RUB ЮMoney
Delets | 1 XRP | 67.0041RUB ЮMoney
КупиБит | 1 XRP | 66.9601RUB ЮMoney
NiceChange | 1 XRP | 66.1776RUB ЮMoney
КэшБанк | 1 XRP | 66.1775RUB ЮMoney
NewLine | 1 XRP | 65.0220RUB ЮMoney
1-Online | 1 XRP | 64.9730RUB ЮMoney
Tec-Bit | 1 XRP | 64.7840RUB ЮMoney
D-Obmen | 1 XRP | 64.1632RUB ЮMoney
Банкомат | 1 XRP | 63.7340RUB ЮMoney
Wiki-Exchange | 1 XRP | 63.6339RUB ЮMoney
YChanger | 1 XRP | 63.5920RUB ЮMoney
BlaBlaChange | 1 XRP | 63.5920RUB ЮMoney
ObmenoFF | 1 XRP | 63.5210RUB ЮMoney
CoinPayMaster | 1 XRP | 63.3475RUB ЮMoney
4ange | 1 XRP | 62.9236RUB ЮMoney
ExchangeKey | 1 XRP | 62.8932RUB ЮMoney
MChange | 1 XRP | 62.7849RUB ЮMoney
Обменко | 1 XRP | 62.7838RUB ЮMoney
GrandChange | 1 XRP | 62.3621RUB ЮMoney
RoyalCash | 1 XRP | 62.3435RUB ЮMoney
RamonCash | 1 XRP | 61.9628RUB ЮMoney
Ex-Money | 1 XRP | 61.2063RUB ЮMoney
ProstoCash | 1 XRP | 61.0132RUB ЮMoney
60сек | 1 XRP | 60.7968RUB ЮMoney
Platov | 1 XRP | 60.3168RUB ЮMoney
BaksMan | 1 XRP | 60.0979RUB ЮMoney
Xchange | 1 XRP | 59.1197RUB ЮMoney
TipTopObmen | 1 XRP | 59.1197RUB ЮMoney
AbcObmen | 1 XRP | 59.1197RUB ЮMoney
OneMoment | 1 XRP | 57.5300RUB ЮMoney
Ферма | 1 XRP | 56.9874RUB ЮMoney
MultiChange | 1 XRP | 55.9051RUB ЮMoney
24PayBank | 1 XRP | 55.9051RUB ЮMoney
AlfaChange | 1 XRP | 55.6421RUB ЮMoney
Bitality | 1 XRP | 52.1625RUB ЮMoney
Ex-Bank | 1 XRP | 49.3700RUB ЮMoney
Crypto-Store | 1 XRP | 47.8860RUB ЮMoney
CoinStart | 1 XRP | 44.2528RUB ЮMoney
"""
