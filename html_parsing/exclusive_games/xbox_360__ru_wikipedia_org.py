#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pandas
import pandas as pd

import requests


url = 'https://ru.wikipedia.org/wiki/Проект:Компьютерные_игры/Списки/Игр_на_Xbox_360'
rs = requests.get(url)

df = pd.read_html(rs.text, header=0)[1]

# na=False -- для игнорирования NaN
exclusive_games_df = df[df['Эксклюзив'].str.contains('(?i)Да|Консоль', na=False)]

result_df = exclusive_games_df[['Название']]
print(result_df.to_string(index=False))
