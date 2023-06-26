#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os


def _search_of_empty_folders(dir, empty_folders):
    has_files = False

    try:
        dir = os.path.normpath(dir)

        for i in os.listdir(dir):
            file_name = os.path.join(dir, i)

            if os.path.isdir(file_name):
                _has_files = _search_of_empty_folders(file_name, empty_folders)

                # Если в внутренних папках файлы, ставим флаг
                if _has_files:
                    has_files = True
                else:
                    empty_folders.append(file_name)
            else:
                has_files = True

    except PermissionError as e:
        print(e)
        # Исключаем папку из списка
        return True

    return has_files


def search_of_empty_folders(dir):
    empty_folders = list()

    _search_of_empty_folders(dir, empty_folders)

    return empty_folders


if __name__ == "__main__":
    path = r"C:\\"

    empty_folders = search_of_empty_folders(path)
    for i in empty_folders:
        print(i)

    # Проверка, что все папки внутри не имеют файлов
    for i in empty_folders:
        for root, dirs, files in os.walk(i):
            if files:
                assert True is False, f"{root}: {files}"
