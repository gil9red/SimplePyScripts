#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Запуск нескольких процессов ffmpeg и ожидание пока все они завершатся."""

# Чтобы убить все процессы ffmpeg в винде: Taskkill /F /IM ffmpeg.exe


videos = [
    'Горит от чатика - Dark Souls #1 176x144.3gp',
    'Горит от чатика - Dark Souls #1 320x180.3gp',
    'Горит от чатика - Dark Souls #1 640x360.mp4',
    'Горит от чатика - Dark Souls #1 640x360.webm',
    'Горит от чатика - Dark Souls #1 1280x720.mp4',
]


DIRECTORY = 'extracted_images'
import os
if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)

COMMAND_PATTERN = 'ffmpeg -ss 01:30:00 -t 1 -i "{file_name}" -r 1 -f image2 "{directory}/{file_name}_%05d.{ext}"'

process_list = list()

for file_name in videos:
    for ext in ['jpg', 'png']:
        command = COMMAND_PATTERN.format(directory=DIRECTORY, file_name=file_name, ext=ext)
        print(command)

        from subprocess import Popen, DEVNULL
        process = Popen(command, stderr=DEVNULL, stdout=DEVNULL)
        process_list.append(process)

while True:
    ok = True

    for process in process_list:
        # Если None, процесс еще не завершился
        if process.poll() is None:
            ok = False
            break

    if ok:
        print("Все процессы завершились")
        break

    import time
    time.sleep(5)
