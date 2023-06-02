#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.pyplot import FormatStrFormatter

import pandas as pd

from bs4 import BeautifulSoup

from download_jira_log import FILE_NAME


data_file = FILE_NAME
root = BeautifulSoup(open(data_file, mode="rb"), "lxml")

records = []
for resolved in root.select("item > resolved"):
    # date local is en_US
    resolved_date_time = datetime.strptime(
        resolved.text.strip(), "%a, %d %b %Y %H:%M:%S %z"
    )
    resolved_year = resolved_date_time.year
    resolved_year_month = datetime(resolved_date_time.year, resolved_date_time.month, 1)

    records.append((resolved_date_time, resolved_year, resolved_year_month))

records.sort(key=lambda x: x[0])

df = pd.DataFrame(
    data=records, columns=["resolved_date_time", "resolved_year", "resolved_year_month"]
)
print(df)
print("Total rows:", len(df))

df_month = pd.DataFrame(
    {"count": df.groupby("resolved_year_month").size()}
).reset_index()
print(df_month)
print()

df_year = pd.DataFrame({"count": df.groupby("resolved_year").size()}).reset_index()
print(df_year)

fig = plt.figure(1)
fig.suptitle("Analysis jira", fontsize=14, fontweight="bold")

ax1 = fig.add_subplot(121)
ax1.plot(df_month["resolved_year_month"], df_month["count"])
ax1.grid()
ax1.set_title("Jira by month")
ax1.set_xlabel("Date")
ax1.set_ylabel("Count")
plt.gcf().autofmt_xdate()

ax2 = fig.add_subplot(122)
ax2.plot(df_year["resolved_year"], df_year["count"])
ax2.ticklabel_format(useOffset=False)
ax2.xaxis.set_major_formatter(FormatStrFormatter("%d"))
ax2.set_title("Jira by year")
ax2.set_xlabel("Date")
ax2.set_ylabel("Count")
ax2.grid()
plt.gcf().autofmt_xdate()

plt.show()
