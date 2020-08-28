#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install jinja2
import jinja2


template = jinja2.Template("""\
<table>
  <tr>
  {% for x in rows_1 %}
    <td>{{ x }}</td>
  {% endfor %}
  </tr>
  <tr>
  {% for x in rows_2 %}
    <td {% if x < 100 %}class="bad"{% endif %}>{{ x }}</td>
  {% endfor %}
  </tr>
</table>
""")


in_dict = {
    'a': [1, 2, 3],
    'b': [3, 4, 5],
    'c': [99, 3],
}

html = template.render(
    rows_1=[k for k, v in in_dict.items()],
    rows_2=[sum(v) for k, v in in_dict.items()]
)
print(html)
"""
<table>
  <tr>
  
    <td>a</td>
  
    <td>b</td>
  
    <td>c</td>
  
  </tr>
  <tr>
  
    <td class="bad">6</td>
  
    <td class="bad">12</td>
  
    <td >102</td>
  
  </tr>
</table>
"""