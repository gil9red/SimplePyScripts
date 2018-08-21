#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import Dict, List

import sys
sys.path.append('..')

from logged_human_time_to_seconds import logged_human_time_to_seconds


def get_date_str_by_entry_logged_list(root) -> Dict[str, List[Dict]]:
    from collections import defaultdict
    date_str_by_entry_logged_list = defaultdict(list)

    for entry in root.select('entry'):
        title = entry.title

        # Содержимое тега title -- экранированное html
        title_node = BeautifulSoup(title.text, 'html.parser')

        title_text = title_node.text.strip()
        title_text = re.sub('\s{2,}', ' ', title_text)

        # Пример: "Ilya A. Petrash logged '30 minutes' on ..."
        match = re.search("Ilya A. Petrash logged '(.+?)'", title_text)
        if not match:
            continue

        logged_human_time = match.group(1)
        logged_seconds = logged_human_time_to_seconds(logged_human_time)

        jira_id = entry.object.title.text.strip()
        jira_title = entry.object.summary.text.strip()

        entry_dt = datetime.strptime(entry.published.text, "%Y-%m-%dT%H:%M:%S.%fZ")
        entry_date = entry_dt.date()
        date_str = entry_date.strftime('%d/%m/%Y')

        date_str_by_entry_logged_list[date_str].append({
            'date_time': entry_dt.strftime('%d/%m/%Y %H:%M:%S'),
            'logged_human_time': logged_human_time,
            'logged_seconds': logged_seconds,
            'jira_id': jira_id,
            'jira_title': jira_title,
        })

    return date_str_by_entry_logged_list


def get_entry_logged_list_by_current_utc_date(date_str_by_entry_logged_list: Dict[str, List[Dict]]) -> List[Dict]:
    current_utc_date_str = datetime.utcnow().strftime('%d/%m/%Y')
    return date_str_by_entry_logged_list.get(current_utc_date_str, [])


def get_logged_total_seconds(entry_logged_list: List[Dict]) -> int:
    return sum(entry['logged_seconds'] for entry in entry_logged_list)


if __name__ == '__main__':
    URL = 'https://jira.compassplus.ru/activity?maxResults=100&streams=user+IS+ipetrash&os_authType=basic&title=undefined'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
    }

    # NOTE. Get <PEM_FILE_NAME>: openssl pkcs12 -nodes -out key.pem -in file.p12
    PEM_FILE_NAME = 'ipetrash.pem'

    import requests
    rs = requests.get(URL, headers=HEADERS, cert=PEM_FILE_NAME)
    print(rs)
    print(len(rs.text), repr(rs.text[:50]))

    open('rs.xml', 'wb').write(rs.content)
    # root = BeautifulSoup(open('rs.xml', 'rb'), 'xml')

    # Структура документа -- xml
    root = BeautifulSoup(rs.content, 'xml')

    date_str_by_entry_logged_list = get_date_str_by_entry_logged_list(root)
    print(date_str_by_entry_logged_list)

    import json
    print(json.dumps(date_str_by_entry_logged_list, indent=4, ensure_ascii=False))
    print()

    from seconds_to_str import seconds_to_str

    entry_logged_list = get_entry_logged_list_by_current_utc_date(date_str_by_entry_logged_list)
    logged_total_seconds = get_logged_total_seconds(entry_logged_list)
    print('entry_logged_list:', entry_logged_list)
    print('today seconds:', logged_total_seconds)
    print('today time:', seconds_to_str(logged_total_seconds))
    print()

    # Для красоты выводим результат в табличном виде
    sorted_items = date_str_by_entry_logged_list.items()
    sorted_items = sorted(sorted_items, key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'), reverse=True)

    lines = []

    for date_str, entry_logged_list in sorted_items:
        total_seconds = get_logged_total_seconds(entry_logged_list)
        lines.append((date_str, total_seconds, seconds_to_str(total_seconds)))

    # Список строк станет списком столбцов, у каждого столбца подсчитается максимальная длина
    max_len_columns = [max(map(len, map(str, col))) for col in zip(*lines)]

    # Создание строки форматирования: [30, 14, 5] -> "{:<30} | {:<14} | {:<5}"
    my_table_format = ' | '.join('{:<%s}' % max_len for max_len in max_len_columns)

    for line in lines:
        print(my_table_format.format(*line))
