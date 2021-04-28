#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт получает список специальностей в формате HTML, разбирает таблицу и оформляет ее в JSON"""


import json
import sys

import requests
from bs4 import BeautifulSoup


def element_to_text_list(el) -> str:
    return ', '.join([child.strip() for child in el.strings])


url = 'http://magtu.ru/modules/mod_abiturient_helper/tmpl/get_spec.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'X-Requested-With': 'XMLHttpRequest',
}

# Русский язык и Математика
post_data = {
    'data': '01,02'
}

rs = requests.post(url, headers=headers, data=post_data)
if not rs.ok or not rs.text:
    print('Post запрос не вернул данные таблицы. Возможно, не хватает каких-то данных.')
    sys.exit()

root = BeautifulSoup(rs.text, 'lxml')
table_rows = []

for tr in root.select('table tr')[1:]:
    td_list = tr.select('td')

    row_data = {
        "number": element_to_text_list(td_list[0]),
        "code": element_to_text_list(td_list[1]),
        "speciality": element_to_text_list(td_list[2]),
        "level_of_education": element_to_text_list(td_list[3]),
        "budget_or_contract": element_to_text_list(td_list[4]),
        "mode_of_study": element_to_text_list(td_list[5]),
        "institute_faculty": element_to_text_list(td_list[6]),
        "list_of_examinations": element_to_text_list(td_list[7]),
    }
    table_rows.append(row_data)

json_text = json.dumps(table_rows, indent=4, ensure_ascii=False, sort_keys=True)
print(json_text)
