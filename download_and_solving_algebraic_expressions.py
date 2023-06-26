#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Скачивание файла
import requests


rs = requests.get(
    "https://cloclo18.datacloudmail.ru/weblink/view/emCb/gXFkchRJ2?etag=7706DA739680EAC4A5B9044E9767047365988F54&key=a91762c6f1d8a559f6d780934b2509c728b33df4"
)

# Получение текста, разделение его построчно, пронумерование
for i, line in enumerate(rs.text.split("\n"), 1):
    # Если строка пустая
    if not line:
        continue

    # Обрезание первого символа, удаление ' ', '\n', '\r' и т.п.
    line = line[1:].strip()
    print(f"{i}. {line} = {eval(line)}")
