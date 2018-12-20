#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from common import get_parsed_two_column_table_stats


url = 'http://ru.darksouls.wikia.com/wiki/Характеристики_(Dark_Souls_II)'
items = get_parsed_two_column_table_stats(url)
print(f'items ({len(items)}): {items}')
print()

for title, description in items:
    print('{:20}: {}'.format(title, repr(description)))
