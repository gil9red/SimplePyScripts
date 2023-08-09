#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"


URL_LOGIN = "http://mywishlist.ru/login/login"

LOGIN = ""
PASSWORD = ""
if not LOGIN or not PASSWORD:
    raise Exception("Логин или пароль не заполнены!")

DATA = {
    "login[login]": LOGIN,
    "login[password]": PASSWORD,
}

rs = session.post(URL_LOGIN, data=DATA)
print(rs.url)  # http://mywishlist.ru/me/ladywerner
rs.raise_for_status()

if "/me/" not in rs.url:
    raise Exception("Не получилось авторизоваться!")

root = BeautifulSoup(rs.content, "html.parser")
user_name = root.select_one(".pProfileMain > h2 > a").text
print(f"user_name: {user_name}")
# user_name: Ladywerner

user_tags = [el.text for el in root.select(".pTagList > span > a")]
print(f"Tags ({len(user_tags)}): {user_tags}")
# Tags (96): ['abh', 'anastasia_beverly_hills', 'beauty', ...

url_friends = rs.url + "/friends/list"
rs = session.get(url_friends)
rs.raise_for_status()

root = BeautifulSoup(rs.content, "html.parser")
user_friends = [el.text for el in root.select(".pFriendList .pProfile a")]
print(f"Friends ({len(user_friends)}): {user_friends}")
# Friends (3): ['Foxmellis', 'Nastiapooh', 'wannabeanarchy']
