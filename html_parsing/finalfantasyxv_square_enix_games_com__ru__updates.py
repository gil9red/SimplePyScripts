#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup, Tag


def get_plaintext(element) -> str:
    if not element:
        return ""

    items = []
    for elem in element.descendants:
        if isinstance(elem, str):
            items.append(elem.strip())
        elif elem.name in ['br', 'p']:
            items.append('\n')
    return ''.join(items).strip()


def parse_ul(ul: Tag, level=1, bullet='•'):
    items = []

    for li in ul.findChildren("li", recursive=False):
        text = li.find(text=True).strip()
        items.append(('  ' * level) + bullet + ' ' + text)

        for sub_ul in li.findChildren("ul", recursive=False):
            items.append(
                parse_ul(sub_ul, level=level+1)
            )

    return '\n'.join(items)


rs = requests.get('https://finalfantasyxv.square-enix-games.com/ru/updates')
root = BeautifulSoup(rs.content, 'html.parser')

for patch in root.select('.patch-notes-text'):
    patch_name_el = patch.select_one('.patch-name')
    patch_name = get_plaintext(patch_name_el)

    game_title_el = patch.select_one('.game-title')
    game_title = get_plaintext(game_title_el).upper()

    ul = patch.select_one("ul")
    text = parse_ul(ul)

    print(patch_name)
    print(game_title)
    print(text)
    print('\n' + '-' * 100 + '\n')

"""
01.04.2020
FINAL FANTASY XV
  • Подлежащие удалению элементы:
    • ИНФОРМАЦИЯ FFXV (информация обновления игры)

----------------------------------------------------------------------------------------------------

01.04.2020
FINAL FANTASY XV WINDOWS EDITION
  • Подлежащие удалению элементы:
    • ИНФОРМАЦИЯ FFXV (информация обновления игры)
    • ГЛАВНОЕ МЕНЮ - ОНЛАЙН
    • ОПЦИИ - ОНЛАЙНОВЫЙ КОНТЕНТ
      • Возможность менять внешность Ноктис
      • Функция отображения теней аватаров других игроков
      • Сокровище игрока
      • Официальное сокровище
      • Подбор игроков в версии для Origin
      • Кроссплатформенный подбор игроков в версиях для Steam и Origin
      • Онлайновый конструктор ОРГАНИЗАТОР МОДОВ
...
"""
