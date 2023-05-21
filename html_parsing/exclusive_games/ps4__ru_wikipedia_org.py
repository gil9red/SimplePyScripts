#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_df_list__no_sub


url = "https://ru.wikipedia.org/wiki/Список_игр_на_Sony_PlayStation_4"
df = get_df_list__no_sub(url)[1]

# na=False -- для игнорирования NaN
exclusive_games_df = df[~df["Эксклюзив"].str.contains("(?i)Нет", na=False)]

result_df = exclusive_games_df[["Название"]]
print(result_df.to_string(index=False))
