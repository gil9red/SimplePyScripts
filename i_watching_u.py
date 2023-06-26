#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Программа делает скриншоты, сохраняет их в zip-архив."""


if __name__ == "__main__":
    import time

    from datetime import datetime
    from io import BytesIO
    from zipfile import ZipFile

    from PIL import ImageGrab

    # Сбор статистики о действиях пользователя

    while True:
        # Текущая дата и время
        today = datetime.today()

        # Получаем строку текущего времени
        str_today_time = today.strftime("%H.%M.%S")

        # Имя zip-архива
        zip_file_name = "screenshots_" + today.strftime("%d.%m.%Y") + ".zip"

        # Составляем имя файла, содержащее в названии текущее время
        file_name = f"screenshot_{str_today_time}.png"

        # Делаем скриншот
        im = ImageGrab.grab()

        print(f'Сделан скриншот "{file_name}"')

        # Открываем zip-файл
        with ZipFile(zip_file_name, "a") as zip_file:
            # Сохраняем изображение в буфер
            io = BytesIO()
            im.save(io, "png")

            # Байты изображения
            image_bytes = io.getvalue()

            # Добавляем изображение в архив
            zip_file.writestr(file_name, image_bytes)

            print(
                f'  Скриншот "{file_name}" добавлен в архив "{zip_file_name}"\n'
            )

        # Ожидание каждые 15 минут
        time.sleep(15 * 60)
