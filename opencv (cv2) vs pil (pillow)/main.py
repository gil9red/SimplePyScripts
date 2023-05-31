#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install opencv-python
# pip install Pillow

import timeit

FILE_NAME = "input.jpg"
NUMBER = 100
GLOBALS = {"FILE_NAME": FILE_NAME}

print("Read image from file:")
print(
    "PIL",
    timeit.timeit(
        "img = Image.open(FILE_NAME)",
        setup="from PIL import Image",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print(
    "CV2",
    timeit.timeit(
        "img = cv2.imread(FILE_NAME)",
        setup="import cv2",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print()

print("Read image from file and get image bytes:")
print(
    "PIL",
    timeit.timeit(
        """\
img = Image.open(FILE_NAME)
bytes_io = io.BytesIO()
img.save(bytes_io, format='JPEG')
img_data = bytes_io.getvalue()
    """,
        setup="from PIL import Image\nimport io",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print(
    "CV2",
    timeit.timeit(
        """\
img = cv2.imread(FILE_NAME)
img_data = cv2.imencode('.jpg', img)[1].tostring()
    """,
        setup="import cv2\nimport io",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print()

print("Invert:")
print(
    "PIL",
    timeit.timeit(
        """\
img = Image.open(FILE_NAME)
img_invert = ImageOps.invert(img)
    """,
        setup="from PIL import Image, ImageOps",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print(
    "CV2",
    timeit.timeit(
        """\
img = cv2.imread(FILE_NAME)
img_invert = cv2.bitwise_not(img)
    """,
        setup="import cv2",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print()

print("Grayscale:")
print(
    "PIL  ",
    timeit.timeit(
        """\
img = Image.open(FILE_NAME)
img_gray = ImageOps.grayscale(img)
    """,
        setup="from PIL import Image, ImageOps",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print(
    "CV2_1",
    timeit.timeit(
        """\
img = cv2.imread(FILE_NAME)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    """,
        setup="import cv2",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print(
    "CV2_2",
    timeit.timeit(
        """\
img_gray = cv2.imread(FILE_NAME, cv2.IMREAD_GRAYSCALE)
    """,
        setup="import cv2",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print()

print("GaussianBlur:")
print(
    "PIL",
    timeit.timeit(
        """\
img = Image.open(FILE_NAME)
img_blur = img.filter(ImageFilter.GaussianBlur(2))
    """,
        setup="from PIL import Image, ImageFilter",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print(
    "CV2",
    timeit.timeit(
        """\
img = cv2.imread(FILE_NAME)
img_blur = cv2.GaussianBlur(img, (15, 15), 0)
    """,
        setup="import cv2",
        number=NUMBER,
        globals=GLOBALS,
    ),
)
print()
