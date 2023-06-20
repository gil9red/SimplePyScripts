#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

from search import search_of_empty_folders


def delete_of_empty_folders(dir, empty_folders=None):
    if empty_folders is None:
        empty_folders = search_of_empty_folders(dir)

    for i in empty_folders:
        print("remove", i)
        try:
            os.rmdir(i)
        except Exception as e:
            print(e)

    print("remove", dir)
    try:
        os.rmdir(dir)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    path = r"1\11\22\33\44\55"

    # Создаем тестовые пустые папки
    os.makedirs(path, exist_ok=True)

    root = "1"
    delete_of_empty_folders(root)
