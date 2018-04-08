#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PIL import Image, ImageOps, ImageFilter
import io


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/4f6d5b013d218cfe5b964af17a2540e2e49adca0/pil_example/invert/main.py
def invert(image):
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        return Image.merge('RGBA', (r2, g2, b2, a))

    else:
        return ImageOps.invert(image)


def gray(img):
    return ImageOps.grayscale(img)


def invert_gray(img):
    img = invert(img)
    return ImageOps.grayscale(img)


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/0f607f2b96b11acc74a678b1dd7d55d9aa3eef73/pil_example/pixelate_image/main.py
def pixelate(image, pixel_size=9, draw_margin=True):
    margin_color = (0, 0, 0)

    image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST)
    image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST)
    pixel = image.load()

    # Draw black margin between pixels
    if draw_margin:
        for i in range(0, image.size[0], pixel_size):
            for j in range(0, image.size[1], pixel_size):
                for r in range(pixel_size):
                    pixel[i+r, j] = margin_color
                    pixel[i, j+r] = margin_color

    return image


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/84651cfefaee768851170ec4ba7d025bbaae622d/get_image_info/main.py
def get_image_info(img, pretty_json_str=True):
    data = io.BytesIO()
    img.save(data, img.format)

    length = len(data.getvalue())

    # Save order
    from collections import OrderedDict
    info = OrderedDict()
    info['length'] = OrderedDict()
    info['length']['value'] = length
    info['length']['text'] = sizeof_fmt(length)

    info['mode'] = img.mode
    info['channels'] = len(img.getbands())
    info['bit_color'] = {
        '1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32,
        'CMYK': 32, 'YCbCr': 24, 'I': 32, 'F': 32
    }[img.mode]

    info['size'] = OrderedDict()
    info['size']['width'] = img.width
    info['size']['height'] = img.height

    if pretty_json_str:
        import json
        info = json.dumps(info, indent=4, ensure_ascii=False)

    return info


def jackal_jpg(img):
    data_io = io.BytesIO()
    img.save(data_io, format='JPEG', quality=1)

    return Image.open(data_io)


def thumbnail(img, size=(128, 128)):
    img.thumbnail(size)
    return img


def blur(img, radius=2):
    return img.filter(ImageFilter.GaussianBlur(radius))
