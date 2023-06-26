#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

import config
from common import get_log_list_by_author


# Название текущего файла без '.py'
plot_title = os.path.basename(__file__)[:-3]

fig = plt.figure(1)
fig.suptitle(plot_title, fontsize=14, fontweight="bold")
ax = fig.add_subplot(111)

author_by_log = get_log_list_by_author(config.SVN_FILE_NAME)

list_top_author_by_log = sorted(
    author_by_log.items(), key=lambda item: len(item[1]), reverse=True
)

# Добавление на график информации о авторах
for author, logs in list_top_author_by_log:
    # Сбор коммитов за месяц/год
    records = [datetime(log.date.year, log.date.month, 1) for log in logs]

    df = pd.DataFrame(data=records, columns=["year_month"])
    df_month = pd.DataFrame({"count": df.groupby("year_month").size()}).reset_index()
    ax.plot(
        df_month["year_month"],
        df_month["count"],
        label=f"{author} ({len(logs)})",
    )

ax.legend()
ax.grid()
ax.set_title("Commits")
ax.set_xlabel("Date")
ax.set_ylabel("Count")

plt.gcf().autofmt_xdate()

plt.show()
