#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from docx import Document
document = Document("Обеденное меню 777.docx")

for table in document.tables:
    for row in table.rows:
        name, weight, price = [i.text.strip() for i in row.cells]
        print('name: {}, weight: {}, price: {}'.format(name, weight, price))

    # Таблицы в меню дублируются
    break
