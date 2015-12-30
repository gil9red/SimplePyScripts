#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Инвертирование цвета картинки"""


if __name__ == '__main__':
    from PIL import Image
    import PIL.ImageOps

    image_file = r"TowerOfGod_s2_ch100_p02_SIU.png_res.jpg"
    image = Image.open(image_file)
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        inverted_image = PIL.ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))
        final_transparent_image.save('new_file.png')
    else:
        inverted_image = PIL.ImageOps.invert(image)
        inverted_image.save('new_name.png')