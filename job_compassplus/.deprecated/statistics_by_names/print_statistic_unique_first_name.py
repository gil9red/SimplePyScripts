#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт для вывода имен без повторений.

"""


from print_statistic_all_names import get_all_names


first_name_list = [name[1] for name in get_all_names(split_name=True)]
print("Total:", len(first_name_list))

unique_first_name_list = list(set(first_name_list))
print(f"Total unique ({len(unique_first_name_list)}): {unique_first_name_list}")
