#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from table_from__html_by_url__wiki__tekken import get_df


df = get_df()

# Столбцы-серии игр: ['Tekken', 'Tekken 2', 'Tekken 3', 'Tekken 4', 'Tekken 5', 'Tekken 6', 'Tekken 7']
cols = [col for col in df.columns if col.startswith("Tekken")]

for index, row in df.iterrows():
    if all(row[col] == "Y" for col in cols):
        print(row[0])
