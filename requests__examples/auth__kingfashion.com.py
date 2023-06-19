#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


data = {
    "login[username]": "yur4enko.vitya@yandex.ru",
    "login[password]": "YEvbpUZ1i5LanIFnxfVW",
}

session = requests.Session()

rs = session.get("https://kingfashion.com/customer/account/")

# Получение поля form_key из формы авторизации
root = BeautifulSoup(rs.content, "lxml")
form_key = root.select_one("#login-form > input[name=form_key]")
data["form_key"] = form_key["value"]

rs = session.post("https://kingfashion.com/customer/account/loginPost/", data=data)
print(rs.url)

root = BeautifulSoup(rs.content, "lxml")
print(root.select_one(".quick-access.shop > .account"))
