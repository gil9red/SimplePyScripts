#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_df_list__no_sub


url = "https://ru.wikipedia.org/wiki/Проект:Компьютерные_игры/Списки/Игр_на_Xbox_360"
df = get_df_list__no_sub(url)[1]

# na=False -- для игнорирования NaN
exclusive_games_df = df[df["Эксклюзив"].str.contains("(?i)Да|Консоль", na=False)]

result_df = exclusive_games_df[["Название"]]
print(result_df.to_string(index=False))
