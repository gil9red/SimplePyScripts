#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


rs = requests.get("https://auto.mail.ru/fuel/ajax/fuel/?rb_id=141")
print(rs.content)
print(rs.json())
