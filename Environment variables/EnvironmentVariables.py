#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os


# Вывести все переменные окружения (environment variables)
print("Environment variables:\n{}".format(os.environ))

print("\nEnvironment variables:")
for var, value in os.environ.items():
    print("'{}': '{}'".format(var, value))

#
# Получение значения переменной окружения Path
env_path = os.environ["Path"]  # или os.environ.get("Path")

# Вывести значение переменной окружения Path
print("\nPath: {}".format(env_path))

# Разделение строки с путями на список
values_env_path = env_path.split(";")
print("Path: {}".format(values_env_path))  # Вывод списка

# Вывод списка путей
print("Path:")
for i, val in enumerate(values_env_path, 1):
    # Если элемент не пустой
    if val:
        print("{}. '{}'".format(i, val) + (": not exist" if not os.path.exists(val) else ""))
