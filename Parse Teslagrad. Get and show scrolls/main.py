#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


# Teslagrad. Прохождение игры на 100%. Карта расположения и изображения свитков (Сайт GamesisArt.ru)

import os
from urllib.parse import urljoin
import requests

# Cache
if not os.path.exists('scrolls.html'):
    rs = requests.get('http://gamesisart.ru/guide/Teslagrad_Prohozhdenie_4.html#Scrolls')
    html = rs.content

    with open('scrolls.html', 'wb') as f:
        f.write(html)

else:
    html = open('scrolls.html', 'rb').read()


URL = 'http://gamesisart.ru/guide/Teslagrad_Prohozhdenie_4.html#Scrolls'
DIR_SCROLLS = 'scrolls'

from bs4 import BeautifulSoup
root = BeautifulSoup(html, 'html.parser')

img_urls = [img['src'] for img in root.select('img[src]')]
img_urls = [urljoin(URL, url_img) for url_img in img_urls if '/Teslagrad_Scroll_' in url_img]
print(len(img_urls), img_urls)

if not os.path.exists(DIR_SCROLLS):
    os.mkdir(DIR_SCROLLS)

# Save images
for url in img_urls:
    rs = requests.get(url)
    img_data = rs.content

    file_name = DIR_SCROLLS + '/' + os.path.basename(url)

    with open(file_name, 'wb') as f:
        f.write(img_data)

# Merge all image into one
IMAGE_WIDTH = 200
IMAGE_HEIGHT = 376
ROWS = 9
COLS = 4

SCROOLS_WIDTH = IMAGE_WIDTH * COLS
SCROOLS_HEIGHT = IMAGE_HEIGHT * ROWS

from PIL import Image
image = Image.new('RGB', (SCROOLS_WIDTH, SCROOLS_HEIGHT))

import glob
file_names = glob.glob('scrolls/*.jpg')

# Sort by <number>: Teslagrad_Scroll_<number>.jpg'
file_names.sort(key=lambda x: int(x.split('.')[0].split('_')[-1]))
it = iter(file_names)

for y in range(0, SCROOLS_HEIGHT, IMAGE_HEIGHT):
    for x in range(0, SCROOLS_WIDTH, IMAGE_WIDTH):
        file_name = next(it)
        img = Image.open(file_name)

        image.paste(img, (x, y))

image.save('scrolls.jpg')
image.show()
