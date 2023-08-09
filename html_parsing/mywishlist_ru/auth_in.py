#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import BASE_URL, do_get, do_post


URL_LOGIN = f"{BASE_URL}/login/login"

LOGIN = ""
PASSWORD = ""
if not LOGIN or not PASSWORD:
    raise Exception("Логин или пароль не заполнены!")

DATA = {
    "login[login]": LOGIN,
    "login[password]": PASSWORD,
}

rs, root = do_post(URL_LOGIN, data=DATA)
print(rs.url)  # http://mywishlist.ru/me/ladywerner

if "/me/" not in rs.url:
    raise Exception("Не получилось авторизоваться!")

user_name = root.select_one(".pProfileMain > h2 > a").text
print(f"user_name: {user_name}")
# user_name: Ladywerner

user_tags = [el.text for el in root.select(".pTagList > span > a")]
print(f"Tags ({len(user_tags)}): {user_tags}")
# Tags (96): ['abh', 'anastasia_beverly_hills', 'beauty', ...

url_friends = rs.url + "/friends/list"
rs, root = do_get(url_friends)

user_friends = [el.text for el in root.select(".pFriendList .pProfile a")]
print(f"Friends ({len(user_friends)}): {user_friends}")
# Friends (3): ['Foxmellis', 'Nastiapooh', 'wannabeanarchy']
