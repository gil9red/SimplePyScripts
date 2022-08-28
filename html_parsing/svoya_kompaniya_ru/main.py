#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import get_menu


url = 'https://magnitogorsk.svoya-kompaniya.ru/'

# TODO: Логирование перенести из get_menu
result = get_menu(url, is_business_lunch=True)
print('\n' + '-' * 100 + '\n')

for full_menu_name, dishes in result.items():
    for dish in dishes:
        print(f'{full_menu_name}: {dish}')
