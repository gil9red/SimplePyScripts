#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_df_list__no_sub


url = "https://ru.wikipedia.org/wiki/Список_игр_на_Xbox_One"
df = get_df_list__no_sub(url)[2]

exclusive_games_df = df[~df["Эксклюзивность"].str.contains("(?i)Microsoft|Нет")]

result_df = exclusive_games_df[["Название", "Жанр(ы)"]]
print(result_df.to_string(index=False))
