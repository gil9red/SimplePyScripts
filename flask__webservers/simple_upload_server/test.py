#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Отправка файла на сервер
import requests


rs = requests.post("http://localhost:6000", files={"file": open("disk_info.txt", "rb")})
print(rs)
