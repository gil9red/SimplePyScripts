#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys

from io import BytesIO
from pathlib import Path

import requests

from PIL import Image

DIR = Path(__file__).resolve().absolute().parent

sys.path.append(str(DIR.parent))
from common import get_chart


qc = get_chart()

# Variant 1
f = BytesIO(qc.get_bytes())
img_chart = Image.open(f)

img = Image.open('input.jpg')
Image.Image.paste(img, img_chart, (10, 10), mask=img_chart)
img.save('input_with_chart_v1.png')

# Variant 2
url = qc.get_url()
raw = requests.get(url, stream=True).raw
img_chart = Image.open(raw)

img = Image.open('input.jpg')
Image.Image.paste(img, img_chart, (10, 10), mask=img_chart)
img.save('input_with_chart_v2.png')
