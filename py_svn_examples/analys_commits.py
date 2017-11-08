#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/dsoprea/PySvn

import svn.local
repo = svn.local.LocalClient('E:/OPTT/optt_trunk')

# OR:
# import svn.remote
# repo = svn.remote.RemoteClient('svn+cplus://svn2.compassplus.ru/twrbs/csm/optt/dev/trunk')

log_list = [log for log in repo.log_default()]
print('Total commits:', len(log_list))

from collections import defaultdict
author_by_log = defaultdict(list)

for log in log_list:
    author_by_log[log.author].append(log)

for author, logs in sorted(author_by_log.items(), key=lambda item: len(item[1]), reverse=True):
    print('    {}: commits {}'.format(author, len(logs)))

print('\n\n')

#
# Draw plot
#

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

import matplotlib.pyplot as plt
fig = plt.figure(1)
ax1 = fig.add_subplot(111)
ax1.plot(df_month['year_month'], df_month['count'])
ax1.grid()
plt.gcf().autofmt_xdate()

plt.show()
