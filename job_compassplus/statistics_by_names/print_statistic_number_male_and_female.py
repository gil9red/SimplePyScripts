#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт для подсчета мужчин и женщин по именам.

"""


# pip install pymorphy2
import pymorphy2

from print_statistic_all_names import get_all_names


name_list = get_all_names(split_name=True)
total = len(name_list)
print('Total:', total)
print()

morph = pymorphy2.MorphAnalyzer()

masc_name_list = []
femn_name_list = []

for _, first_name, _ in name_list:
    parsed_word_list = morph.parse(first_name)
    parsed_word = None

    if len(parsed_word_list) > 1:
        parsed_word_list_filtered = list(filter(lambda x: x.normal_form.lower() == first_name.lower(), parsed_word_list))
        if not parsed_word_list_filtered:
            # Алена -> Алёна
            parsed_word_list_filtered = list(filter(lambda x: x.normal_form.lower() == first_name.lower().replace('е', 'ё'), parsed_word_list))
            if not parsed_word_list_filtered:
                print('Error by parsing name:', first_name.upper(), parsed_word_list)
                continue

            parsed_word = parsed_word_list_filtered[0]
        else:
            parsed_word = parsed_word_list_filtered[0]
    else:
        parsed_word = parsed_word_list[0]

    gender = parsed_word.tag.gender

    if gender == 'masc':
        masc_name_list.append(first_name)
    else:
        femn_name_list.append(first_name)

# Сортировка списка имен
masc_name_list.sort()
femn_name_list.sort()

print(f'Masc ({len(masc_name_list)}): {masc_name_list}')
print(f'Femn ({len(femn_name_list)}): {femn_name_list}')
