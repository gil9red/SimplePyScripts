#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "ipetrash"


import re


def get_cache_object_info(file_name) -> dict[str, dict[str, int]]:
    # new_object: Tran[180409000010273756]
    # existing_object: Hold[13708]
    pattern_object = re.compile(r"^(\w+_object): (.+)\[.+$")

    object_by_number = dict()

    for line in open(file_name):
        match = pattern_object.search(line)
        if match:
            type_cache = match[1]
            name = match[2]

            if type_cache not in object_by_number:
                object_by_number[type_cache] = dict()

            if name not in object_by_number[type_cache]:
                object_by_number[type_cache][name] = 0

            object_by_number[type_cache][name] += 1

    return object_by_number


def get_cache_existing_object_list(
    file_name, top_values=None
) -> list[tuple[str, int]]:
    object_by_number = get_cache_object_info(file_name)

    existing_object_list = sorted(
        object_by_number["existing_object"].items(), key=lambda x: x[1], reverse=True
    )
    if top_values:
        existing_object_list = existing_object_list[:top_values]

    rows = [(name, number) for name, number in existing_object_list]
    return rows


if __name__ == "__main__":
    file_name = "CacheContent_log.txt"
    print(file_name)

    rows = get_cache_existing_object_list(file_name, top_values=5)

    # pip install tabulate
    from tabulate import tabulate
    print(tabulate(rows, headers=("NAME", "NUMBER"), tablefmt="grid"))
