#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pandas as pd


# SOURCE: https://ru.stackoverflow.com/a/846931/201445
json_data = {
    "items": [
        {"first_name": "Оля", "id": 111111, "last_name": "Сущенко"},
        {"first_name": "Георгий", "id": 222222, "last_name": "Голосов"},
        {
            "first_name": "Максим",
            "id": 333333,
            "home_phone": "+79909999999",
            "last_name": "Тупиченков",
        },
    ]
}

df = pd.io.json.json_normalize(json_data["items"])
print(df)

df.to_csv("out.csv", index=False)
