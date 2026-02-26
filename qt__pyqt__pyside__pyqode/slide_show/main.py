#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# TODO:
"""Задание:
Нужно создать приложение слайд-шоу, которое должно иметь следующие основные
особенность: показывать изображения, сдвигая их по истечении определенного периода времени.
Хотя нет никаких строгих требований к UI, приложение должно быть
удобный. Там также должен быть отдельный экран с настройками приложения
доступны из главного меню экрана слайд-шоу.

Базовые требования:
- пользователь должен иметь возможность выбрать источник данных из папки, расположенной либо
во внутренней памяти или на SD-карте;
- пользователь должен иметь возможность установить длину переключения (от 1 до 60 секунд)
между изображениями;
- изображение должно отображаться в полноэкранном режиме, сохраняя при этом аспект
отношение.

То, что мы действительно хотели бы видеть:
1. "Выберите из интернета" вариант (5-6 изображений макс) при выборе данных
источник. Подготовьте URL-адреса заранее, при скольжении к следующему экране
соответствующее изображение должно быть в асинхронном режиме, загруженных из Интернета
а затем показано на рисунке. Во время процесса горизонтальный процесс загрузки бар
должен появиться.
2. Пользователь должен иметь возможность сохранить все настройки в памяти устройства.
3. По крайней мере, пару скользящих эффектов, например, "Исчезать / проявки" и "слева направо".
Код приложения должны быть загружены в хранилище на общественном Github, так что один
мог взять его и компилировать. Аспекты, которые будут оцениваться:
- полнота реализации задач;
- удобство пользовательского интерфейса;
- простота и читаемость кода.
"""


import sys

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QTimer, Qt


# TODO: использовать машину состоний для упрощения алгоритма
# TODO: вариант перехода к следующему слайду: effect_of_vanishing_photos/effect_of_vanishing_photos.py


class SlideShowWidget(QWidget):
    def __init__(self, image_list: list[str]) -> None:
        super().__init__()

        self.setWindowTitle("SlideShowWidget")

        self.current_index = 0
        self.source_image = None
        self.resize_image = None

        self.timer = QTimer()
        self.timer.setInterval(60 * 1000)
        self.timer.timeout.connect(self.next)

        self.image_list = image_list
        self.next()

        self.resize(200, 200)

    def set_timeout(self, timeout) -> None:
        self.timer.setInterval(timeout * 1000)
        self.timer.start()

    def next(self) -> None:
        if not self.image_list:
            return

        self.source_image = QPixmap(self.image_list[self.current_index])
        self.resize_image = self.source_image.scaled(self.size(), Qt.KeepAspectRatio)
        self.update()

        self.current_index += 1
        if self.current_index >= len(self.image_list):
            self.current_index = 0

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

        if self.source_image:
            self.resize_image = self.source_image.scaled(
                self.size(),
                Qt.KeepAspectRatio,
            )

    def paintEvent(self, event) -> None:
        if self.source_image is None:
            super().paintEvent(event)
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(Qt.black)
        painter.drawRect(self.size())
        painter.drawPixmap(0, 0, self.resize_image)


if __name__ == "__main__":
    import glob
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # TODO:
    image_list = glob.glob(r"C:\Users\ipetrash\Pictures\*.png")

    w = SlideShowWidget(image_list)
    w.set_timeout(1)
    w.show()

    sys.exit(app.exec_())
