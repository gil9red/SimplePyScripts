#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PIL import Image, ImageOps, ImageFilter
import io


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/4f6d5b013d218cfe5b964af17a2540e2e49adca0/pil_example/invert/main.py
def invert(image):
    if image.mode == "RGBA":
        r, g, b, a = image.split()
        rgb_image = Image.merge("RGB", (r, g, b))
        inverted_image = ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        return Image.merge("RGBA", (r2, g2, b2, a))

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

    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    pixel = image.load()

    # Draw black margin between pixels
    if draw_margin:
        for i in range(0, image.size[0], pixel_size):
            for j in range(0, image.size[1], pixel_size):
                for r in range(pixel_size):
                    pixel[i + r, j] = margin_color
                    pixel[i, j + r] = margin_color

    return image


def jackal_jpg(img):
    data_io = io.BytesIO()
    img.save(data_io, format="JPEG", quality=1)

    return Image.open(data_io)


def thumbnail(img, size=(128, 128)):
    img.thumbnail(size)
    return img


def blur(img, radius=2):
    return img.filter(ImageFilter.GaussianBlur(radius))
