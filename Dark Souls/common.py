#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_transitions_location(url_location: str) -> list:
    """
    Функция для поиска переходов из локации

    """

    rs = requests.get(url_location)
    root = BeautifulSoup(rs.content, 'html.parser')

    transitions = []

    table_transitions = root.select_one('table.pi-horizontal-group')
    if not table_transitions or 'Переходы:' not in table_transitions.text:
        return transitions

    for a in table_transitions.select('a'):
        url = urljoin(rs.url, a['href'])

        transitions.append((url, a.text.strip()))

    return transitions
