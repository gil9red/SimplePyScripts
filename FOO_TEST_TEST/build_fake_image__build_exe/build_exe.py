#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://habr.com/post/126198/
# SOURCE: http://www.fileformat.info/info/unicode/char/202E/index.htm


# TODO: этот частный случай, сделать общий -- возможность засунуть любой файл

# TODO: generate image_png.py: https://github.com/gil9red/SimplePyScripts/blob/aec64c1749d4f6f3176e3222c7e7c554f40c693f/generator_py_with_inner_image_with_open/main.py
# TODO: convert image to ico


import subprocess
import zipfile
import shutil


FILE_NAME = 'main.exe'

# Юникодная последовательсть \u202E нужна чтобы превратить: picgpj.exe -> pic‮gpj.exe
NEW_FILE_NAME = 'pic\u202Egpj.exe'

FILE_NAME_ARCHIVE = 'pic.zip'

# Analog build_exe.bat
subprocess.call(["pyinstaller", "--onefile", "--noconsole", "--icon=icon.ico", "--name=" + FILE_NAME, "main.py"])

shutil.copy('dist/' + FILE_NAME, 'dist/' + NEW_FILE_NAME)

# Добавляем файл в архив
with zipfile.ZipFile('dist/' + FILE_NAME_ARCHIVE, mode='w', compression=zipfile.ZIP_DEFLATED) as f:
    f.write('dist/' + NEW_FILE_NAME, NEW_FILE_NAME)
