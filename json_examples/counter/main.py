#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json


file_name = "counter.json"

json_data = json.load(open(file_name, encoding="utf-8"))
print(json_data)

# Изменение объекта
json_data["counter"] += 1

# Сохранение
json.dump(json_data, open(file_name, mode="w", encoding="utf-8"))
