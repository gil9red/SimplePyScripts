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


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


with open(file_name_dir + '/' + 'disk_info.txt', 'w', encoding='utf-8') as f:
    # pip install psutil
    import psutil

    f.write('Disk partitions:\n')

    for disk in psutil.disk_partitions():
        f.write('    {}\n'.format(disk))

    f.write('\n')

    f.write('Disk usage:\n')
    for disk in filter(lambda x: 'fixed' in x.opts, psutil.disk_partitions()):
        info = psutil.disk_usage(disk.device)
        f.write('    {} {}\n'.format(disk.device, info))
        f.write('        {} free of {}\n'.format(sizeof_fmt(info.free), sizeof_fmt(info.total)))
        f.write('\n')
