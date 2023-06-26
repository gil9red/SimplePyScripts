#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт, используя сервис http://sms.ru, отправляет смс."""


# Описание API: https://mts.sms.ru/?panel=api&subpanel=method&show=sms/send


import requests


api_id = "<api_id>"
to = "<to>"
text = "<text>"

url_pattern = "http://sms.ru/sms/send?api_id={api_id}&to={to}&text={text}"

rs = requests.get(url_pattern.format(api_id=api_id, to=to, text=text))
print(rs)
print(rs.text)
