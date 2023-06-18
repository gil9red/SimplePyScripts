#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт для авторизации на github вручную"""


import requests
from lxml import etree


LOGIN = "<LOGIN>"
PASSWORD = "<PASSWORD>"


session = requests.Session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"

rs = session.get("https://github.com")
print(rs)

rs = session.get("https://github.com/login")
print(rs)

root = etree.HTML(rs.content)

input_name_by_value = dict()
for input_tag in root.xpath("//input"):
    try:
        input_name_by_value[input_tag.attrib["name"]] = input_tag.attrib["value"]
    except KeyError:
        pass

input_name_by_value["login"] = LOGIN
input_name_by_value["password"] = PASSWORD

rs = session.post("https://github.com/session", data=input_name_by_value)
print(rs)

rs = session.get("https://github.com/gil9red/search_in_users_github_gists")
print(rs)
print(rs.text)
