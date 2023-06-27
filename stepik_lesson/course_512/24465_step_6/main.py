#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Вам дана в архиве (main.zip) файловая структура, состоящая из директорий и файлов.

Вам необходимо распаковать этот архив, и затем найти в данной в файловой структуре все директории, в которых есть
хотя бы один файл с расширением ".py".

Ответом на данную задачу будет являться файл со списком таких директорий, отсортированных в лексикографическом порядке.

Для лучшего понимания формата задачи, ознакомьтесь с примером.
sample.zip
sample_ans.txt
"""


if __name__ == "__main__":
    import zipfile
    import os.path

    with zipfile.ZipFile("main.zip") as zf:
        # Фильтруем список, оставляя только файлы формата .py
        py_file_list = filter(lambda x: x.filename.endswith(".py"), zf.infolist())

        # Получение директорий файлов и удаление дубликатов
        py_file_list = {
            os.path.dirname(file_info.filename) for file_info in py_file_list
        }

        # Сортировка
        py_file_list = sorted(py_file_list)

        with open("main_ans.txt", "w") as f:
            for file_name in py_file_list:
                print(file_name)
                print(file_name, file=f)
