#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://habr.com/post/126198/
# SOURCE: http://www.fileformat.info/info/unicode/char/202E/index.htm


# TODO: этот частный случай, сделать общий -- возможность засунуть любой файл

# TODO: generate image_png.py: https://github.com/gil9red/SimplePyScripts/blob/aec64c1749d4f6f3176e3222c7e7c554f40c693f/generator_py_with_inner_image_with_open/main.py
# TODO: convert image to ico
# TODO: append to zip

# Analog build_exe.bat
import subprocess
subprocess.call(["pyinstaller", "--onefile", "--noconsole", "--icon=icon.ico", "--name=main", "main.py"])

import shutil
shutil.copy('dist/main.exe', 'dist/pic\u202Egpj.exe')
