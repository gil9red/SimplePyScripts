#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests


rs = requests.get("https://ru.stackoverflow.com")
print(rs.cookies.get_dict())
# {'prov': '<...>'}

print()

session = requests.session()
rs = session.get("https://ru.stackoverflow.com")
print(rs.cookies.get_dict())
print(session.cookies.get_dict())
# {'prov': '<...>'}
# {'prov': '<...>'}

rs = session.get("https://google.ru")
print(rs.cookies.get_dict())
print(session.cookies.get_dict())
# {'1P_JAR': '<...>', 'NID': '<...>'}
# {'1P_JAR': '<...>', 'NID': '<...>', 'prov': '<...>'}

print()
print(session.cookies.get_dict(".google.ru"))
# {'1P_JAR': '<...>', 'NID': '<...>'}
