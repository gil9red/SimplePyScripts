#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64

from os.path import exists, join, abspath
from os import makedirs

import jinja2

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def img_to_src_base64(file_name: str) -> str:
    src_text = "data:image/png;base64,"

    if not exists(file_name):
        return src_text

    with open(file_name, "rb") as f:
        img_bytes = f.read()

    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    return src_text + img_base64


DIR_NAME = "output"
makedirs(DIR_NAME, exist_ok=True)


with open("input/template__index.html", encoding="utf-8") as f:
    TEMPLATE__INDEX = jinja2.Template(f.read())


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)  # seconds

try:
    for title, img1, img2, img3 in [
        ("Title", 1, 2, 3),
        ("Hello World", 3, 1, 2),
        ("Not found: 777.png", 1, 777, 3),
    ]:
        file_name = f"index_{img1}_{img2}_{img3}.html"
        file_name = abspath(join(DIR_NAME, file_name))

        # Render HTML and save in file
        with open(file_name, "w", encoding="utf-8") as f:
            img1 = img_to_src_base64(f"input/{img1}.png")
            img2 = img_to_src_base64(f"input/{img2}.png")
            img3 = img_to_src_base64(f"input/{img3}.png")

            html = TEMPLATE__INDEX.render(
                title=title, img_1=img1, img_2=img2, img_3=img3
            )
            f.write(html)

        driver.get("file:///" + file_name)
        print(f'Title: "{driver.title}"')

        with open(file_name + ".png", "wb") as f:
            image_data = driver.find_element(By.ID, "screenshot_this").screenshot_as_png
            f.write(image_data)

finally:
    driver.quit()
