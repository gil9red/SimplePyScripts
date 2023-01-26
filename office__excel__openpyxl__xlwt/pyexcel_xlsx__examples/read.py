#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
from pathlib import Path

# pip install pyexcel-xlsx
from pyexcel_xlsx import read_data


DIR = Path(__file__).resolve().parent
file_name = str(DIR / "output.xlsx")


data = read_data(file_name)
print(json.dumps(data, ensure_ascii=False, indent=4))
"""
{
    "Sheet 1": [
        [
            "Col1",
            "Col2",
            "Col3"
        ],
        [
            1,
            2,
            3
        ],
        [
            4,
            5,
            6
        ]
    ],
    "Sheet 2": [
        [
            "row 1",
            "row 2",
            "row 3"
        ]
    ],
    "Страница 3": [
        [
            "Поле:",
            "Привет"
        ],
        [
            "Поле:",
            "Мир!"
        ]
    ]
}
"""
