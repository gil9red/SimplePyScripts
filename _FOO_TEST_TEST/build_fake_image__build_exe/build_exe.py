#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://habr.com/post/126198/
# SOURCE: http://www.fileformat.info/info/unicode/char/202E/index.htm


# TODO: этот частный случай, сделать общий -- возможность засунуть любой файл


import subprocess
import zipfile
import shutil
import os
import generator


FILE_NAME = 'image.jpg'
FILE_NAME_ICO = 'icon.ico'
ICON_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64)]

OUT_FILE_NAME = 'main.exe'

# Юникодная последовательсть \u202E нужна чтобы превратить: picgpj.exe -> pic‮gpj.exe
NEW_FILE_NAME = 'pic\u202Egpj.exe'

FILE_NAME_ARCHIVE = 'pic.zip'


# Создадим ico файл для иконки приложения
generator.convert_image_to_ico(FILE_NAME, FILE_NAME_ICO, ICON_SIZES)

# Cгенерируем python-файл с картинкой
generator.generate(FILE_NAME)

# Analog build_exe.bat
subprocess.call(
    ["pyinstaller", "--onefile", "--noconsole", "--icon=" + FILE_NAME_ICO, "--name=" + OUT_FILE_NAME, "main.py"]
)

# Подчистим за собой, удалив ненужные файлы
os.remove(FILE_NAME_ICO)
os.remove(generator.FILE_NAME)


shutil.copy('dist/' + OUT_FILE_NAME, 'dist/' + NEW_FILE_NAME)

# Добавляем файл в архив
with zipfile.ZipFile('dist/' + FILE_NAME_ARCHIVE, mode='w', compression=zipfile.ZIP_DEFLATED) as f:
    f.write('dist/' + NEW_FILE_NAME, NEW_FILE_NAME)
