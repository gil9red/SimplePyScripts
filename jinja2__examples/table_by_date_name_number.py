#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime
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

result = dict()
for dt, name in array1:
    date = dt.date()
    if date not in result:
        result[date] = dict()
    result[date][name] = result[date].get(name, 0) + 1

name_by_results = dict()
for i, (date, name_by_number) in enumerate(result.items()):
    for name, number in name_by_number.items():
        if name not in name_by_results:
            name_by_results[name] = [""] * len(result)

        name_by_results[name][i] = number


template = jinja2.Template("""\
<table class="table-2">
  <tr>
    <td>Отчет</td>
  {% for x in header %}
    <td>{{ x }}</td>
  {% endfor %}
  </tr>
  {% for row in rows %}
    <tr>
        {% for x in row %}        
        <td>{{ x }}</td>
        {% endfor %}
    </tr>
  {% endfor %}
</table>
""")

unique_name = sorted(name_by_results)
rows = []
for name in unique_name:
    rows.append([name] + name_by_results[name])

html_tab = template.render(
    header=result.keys(),
    rows=rows,
)
print(html_tab)
