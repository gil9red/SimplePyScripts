#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://pikabu.ru/page/interview/fullstack/
# 19. Секретный агент Пикабу передал зашифрованное изображение. Вам необходимо расшифровать изображение и вывести его
# на страницу средствами JS (без сторонних библиотек). Алгоритм дешифрования известен:
#     * пиксели перебираются слева направо для каждой строки;
#     * для каждого пикселя вычисляется параметр s += x + y * 80 (изначально s = 0 и для каждого следующего пикселя
#       значение увеличивается на x + y * 80), где x - колонка пикселя, y - строка;
#     * для канала красного и синего цвета необходимо добавить параметр s;
#     * для канала зеленого цвета необходимо отнять параметр s следующим образом: green = (green - s) & 0xff;


# pip install Pillow
from PIL import Image

image = Image.open('154800137443598227.png')
width, height = image.size
pixel = image.load()

s = 0

for y in range(height):
    for x in range(width):
        s += x + y * 80

        # RGBa, alpha-канал нас не интересует, только RGB
        r, g, b, _ = pixel[x, y]

        r = (r + s) & 0xff
        g = (g - s) & 0xff
        b = (b + s) & 0xff

        pixel[x, y] = r, g, b


image.save('result.png')
