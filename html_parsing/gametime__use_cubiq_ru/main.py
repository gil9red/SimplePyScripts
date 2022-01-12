#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from dataclasses import dataclass
from typing import Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


@dataclass
class Time:
    text: str
    seconds: int

    @classmethod
    def from_text(cls, value: str) -> 'Time':
        seconds = to_seconds(value)
        return cls(value, seconds)


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'

session = requests.Session()
session.headers['User-Agent'] = USER_AGENT


def to_seconds(time_str: str) -> int:
    kind_to_seconds = {
        'ч': 60 * 60,
        'мин': 60,
    }

    seconds = 0
    for value, kind in re.findall(r'(\d+) (ч|мин)', time_str):
        if kind not in kind_to_seconds:
            raise Exception(f'Неизвестный kind={kind}!')

        seconds += int(value) * kind_to_seconds[kind]

    return seconds


# SOURCE: https://github.com/gil9red/price_of_games/blob/9311f9cbc6b9e57d0308436e3dbf3e524f23ef74/app_parser/utils.py
def smart_comparing_names(name_1: str, name_2: str) -> bool:
    """
    Функция для сравнивания двух названий игр.
    Возвращает True, если совпадают, иначе -- False.

    """

    # Приведение строк к одному регистру
    name_1 = name_1.lower()
    name_2 = name_2.lower()

    def remove_postfix(text: str) -> str:
        for postfix in ('dlc', 'expansion'):
            if text.endswith(postfix):
                return text[:-len(postfix)]
        return text

    # Удаление символов кроме буквенных, цифр и _: "the witcher®3:___ вася! wild hunt" -> "thewitcher3___васяwildhunt"
    def clear_name(name: str) -> str:
        return re.sub(r'\W', '', name)

    name_1 = clear_name(name_1)
    name_1 = remove_postfix(name_1)

    name_2 = clear_name(name_2)
    name_2 = remove_postfix(name_2)

    return name_1 == name_2


def get(url: str) -> Dict[str, Dict[str, Time]]:
    rs = session.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    data = {
        'title': root.select_one('.entry-header').get_text(strip=True),
    }

    for li in root.select('ul.game_times > li'):
        name = li.h5.get_text(strip=True)
        value = li.div.get_text(strip=True)

        data[name] = Time.from_text(value)

    return data


def find(game: str) -> Optional[Dict[str, Dict[str, Time]]]:
    url_search = 'https://cubiq.ru/gametime/?s=' + game

    rs = session.get(url_search)
    root = BeautifulSoup(rs.content, 'html.parser')

    for a in root.select('.entry-title > a[href]'):
        name = a.get_text(strip=True)
        if smart_comparing_names(name, game):
            url = urljoin(rs.url, a['href'])
            return get(url)


if __name__ == '__main__':
    assert to_seconds('25 ч. 18 мин.') == 91080
    assert to_seconds('71 ч. 50 мин.') == 258600
    assert to_seconds('113 ч.') == 406800

    url = 'https://cubiq.ru/gametime/age-of-wonders-iii/'
    rs = get(url)
    print(rs)
    # {
    #      'title': 'Время прохождения Age of Wonders III',
    #      'Основной сюжет': Time(text='25 ч. 18 мин.', seconds=91080),
    #      'Cюжет и доп. задания': Time(text='71 ч. 50 мин.', seconds=258600),
    #      'Перфекционист': Time(text='113 ч.', seconds=406800)
    #  }

    print()
    print(find('dead space'))
    # {
    #     'title': 'Время прохождения Dead Space',
    #     'Основной сюжет': Time(text='11 ч. 10 мин.', seconds=40200),
    #     'Cюжет и доп. задания': Time(text='13 ч. 10 мин.', seconds=47400),
    #     'Перфекционист': Time(text='20 ч. 41 мин.', seconds=74460)
    # }

    print()
    print(find('dead space 2'))
    # {
    #     'title': 'Время прохождения Dead Space 2',
    #     'Основной сюжет': Time(text='9 ч. 18 мин.', seconds=33480),
    #     'Cюжет и доп. задания': Time(text='11 ч. 49 мин.', seconds=42540),
    #     'Перфекционист': Time(text='17 ч. 23 мин.', seconds=62580)
    # }
