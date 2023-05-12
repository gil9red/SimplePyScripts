#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


# Текущая папка, где находится скрипт
DIR = Path(__file__).resolve().parent

# Создание папки для базы данных
DB_DIR_NAME = DIR / "database"
DB_DIR_NAME.mkdir(parents=True, exist_ok=True)

# Путь к файлу базы данных
DB_FILE_NAME = str(DB_DIR_NAME / "database.sqlite")

# Максимальная длина идентификаторов ссылок
LENGTH_URL_ID: int = 5
