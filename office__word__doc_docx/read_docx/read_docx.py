#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

# pip install python-docx
from docx import Document


document = Document("Обеденное меню 777.docx")

# Регулярка для поиска последовательностей пробелов: от двух подряд и более
multi_space_pattern = re.compile(r" {2,}")

for table in document.tables:
    for row in table.rows:
        name, weight, price = [
            multi_space_pattern.sub(" ", i.text.strip()) for i in row.cells
        ]

        if name == weight == price or (not weight or not price):
            print()
            name = name.title()
            print(name)
            continue

        print(f"{name} {weight} {price}")

    # Таблицы в меню дублируются
    break
