#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import time

from threading import Thread

from flask import Flask


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


text = "Hello World!"


def go() -> None:
    time.sleep(2)
    print("\n")

    global text

    while True:
        text = input(f'Current text is "{text}". New next: ')


@app.route("/")
def index():
    return text


if __name__ == "__main__":
    thread = Thread(target=go)
    thread.start()

    # app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
