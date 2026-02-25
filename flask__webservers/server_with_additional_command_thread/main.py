#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import time

from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup
from flask import Flask, request, redirect


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


COMMAND_TEXT = None
EXECUTE_COMMAND = False


@app.route("/")
def index():
    return redirect("/img_search?text=Котята")


@app.route("/img_search")
def img_search():
    text = request.args.get("text")
    print("text:", text)

    global EXECUTE_COMMAND, COMMAND_TEXT
    COMMAND_TEXT = text
    EXECUTE_COMMAND = False

    return "text: " + text


def loop_command_function() -> None:
    while True:
        global EXECUTE_COMMAND, COMMAND_TEXT

        if not EXECUTE_COMMAND and COMMAND_TEXT:
            print(COMMAND_TEXT)

            url = "http://yandex.ru/images/search?text=" + COMMAND_TEXT

            rs = requests.get(url)
            print(rs)

            root = BeautifulSoup(rs.content, "lxml")

            img_list = []
            for img in root.select("img.serp-item__thumb"):
                url_img = urljoin(url, img["src"])
                img_list.append(url_img)

            print(f"img_list[{len(img_list)}]: {img_list}")

            EXECUTE_COMMAND = True

        time.sleep(1)


if __name__ == "__main__":
    from threading import Thread

    thread = Thread(target=loop_command_function)
    thread.start()

    # Localhost
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
