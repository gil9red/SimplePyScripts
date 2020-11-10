#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime
from collections import defaultdict

import jinja2


array1 = [
    [datetime.datetime(2020, 10, 27, 12, 37), 'Саша'],
    [datetime.datetime(2020, 10, 28, 16, 2), 'Олег'],
    [datetime.datetime(2020, 10, 27, 16, 40), 'Саша'],
    [datetime.datetime(2020, 10, 27, 16, 41), 'Саша'],
    [datetime.datetime(2020, 10, 27, 12, 54), 'Костя'],
    [datetime.datetime(2020, 10, 27, 12, 27), 'Костя'],
    [datetime.datetime(2020, 10, 27, 12, 27), 'Олег'],
    [datetime.datetime(2020, 10, 27, 12, 54), 'Саша']
]

result = defaultdict(dict)
dates = set()

for dt, name in array1:
    date = dt.date()

    if name not in result:
        result[name] = dict()

    if date not in result[name]:
        result[name][date] = 0

    result[name][date] += 1
    dates.add(date)


template = jinja2.Template("""\
<table class="table-2">
  <tr>
    <td>Отчет</td>
  {% for date in dates %}
    <td>{{ date }}</td>
  {% endfor %}
  </tr>
  {% for name, date_by_number in result.items() %}
    <tr>
        <td>{{ name }}</td>
      {% for date in dates %}
        <td>{{ date_by_number.get(date, "") }}</td>
      {% endfor %}
    </tr>
  {% endfor %}
</table>
""")

html_tab = template.render(
    dates=sorted(dates),
    result=result,
)
print(html_tab)
