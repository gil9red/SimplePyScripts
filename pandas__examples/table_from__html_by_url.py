#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pandas
import pandas as pd


url = "http://www.gks.ru/bgd/regl/b12_14p/IssWWW.exe/Stg/d01/05-02.htm"
df = pd.read_html(url, header=0, index_col=0)[0]
print(df)

df.to_excel("table.xlsx")
