#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pandas
import pandas as pd

# pip install requests
import requests

# pip install bs4
from bs4 import BeautifulSoup


def get_df():
    url = "https://ru.wikipedia.org/wiki/Список_персонажей_Tekken"
    rs = requests.get(url)

    # Удаление сносок -- из-за них имена персонажей и значения присутствия в конкретной серии показывается
    # невалидно, например "Акума14", а не "Акума"
    root = BeautifulSoup(rs.content, "html.parser")
    for sub in root.select("sup"):
        sub.decompose()

    df_list = pd.read_html(str(root), header=0)
    return df_list[0]


if __name__ == "__main__":
    df = get_df()
    print(df)

    df.to_excel("tekken_table.xlsx", index=False)
