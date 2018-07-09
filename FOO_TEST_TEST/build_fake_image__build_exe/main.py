#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))
    print(text)

    with open('error.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    quit()


import sys
sys.excepthook = log_uncaught_exceptions


# Сохраняем из скрипта картинку и открываем ее через ассоциированную программу
import image_png
image_png.save_and_run()

# ------------------------------------------------------

# Составление пути в папку APPDATA
import os
app_data_dir = os.getenv('APPDATA')
file_name_dir = os.path.normpath(os.path.join(app_data_dir, 'Сорок/тысяч/обезьян/в жопу/сунули/банан'))

# Создаем папки
if not os.path.exists(file_name_dir):
    os.makedirs(file_name_dir)

# Сохраняем скриншот
from PIL import ImageGrab
im = ImageGrab.grab()
im.save(file_name_dir + '/' + 'screenshot.png')

import time
for i in range(1, 10 + 1):
    time.sleep(1)

    file_name = file_name_dir + '/' + '{}.txt'.format(i)
    with open(file_name, 'w', encoding='utf-8') as f:
        pass

# Сохраняем сообщение в файле
file_name = file_name_dir + '/' + 'Прочти это!.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write('Прикольно ведь, а? :)')
