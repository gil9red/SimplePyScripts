#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from analys_commits import get_log_list_by_author
author_by_log = get_log_list_by_author()

records = []

from datetime import datetime

for log in author_by_log['ipetrash']:
    year_month = datetime(log.date.year, log.date.month, 1)
    records.append((log.date, year_month))

import pandas as pd
df = pd.DataFrame(data=records, columns=['date', 'year_month'])
print(df)
print('Total rows:', len(df))

df_month = pd.DataFrame({'count': df.groupby("year_month").size()}).reset_index()
print(df_month)
print()

# Название текущего файла без '.py'
import os
plot_title = os.path.basename(__file__)[:-3]

import matplotlib.pyplot as plt
fig = plt.figure(1)
fig.suptitle(plot_title, fontsize=14, fontweight='bold')

ax = fig.add_subplot(111)
ax.plot(df_month['year_month'], df_month['count'])
ax.grid()
ax.set_title('Commits')
ax.set_xlabel('Date')
ax.set_ylabel('Count')

plt.gcf().autofmt_xdate()

plt.show()
