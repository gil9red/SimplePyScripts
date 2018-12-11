#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pandas
import pandas as pd

import requests


url = 'https://ru.wikipedia.org/wiki/Список_игр_на_Xbox_One'
rs = requests.get(url)

df = pd.read_html(rs.text, header=0)[2]

exclusive_games_df = df[~df['Эксклюзивность'].str.contains('(?i)Microsoft|Нет')]

result_df = exclusive_games_df[['Название', 'Жанр(ы)']]
print(result_df.to_string())
