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

    # Структура документа -- xml
    root = BeautifulSoup(rs.content, 'xml')

    date_str_by_entry_logged_list = get_date_str_by_entry_logged_list(root)
    print(date_str_by_entry_logged_list)

    import json
    print(json.dumps(date_str_by_entry_logged_list, indent=4, ensure_ascii=False))
