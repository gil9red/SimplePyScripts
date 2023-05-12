#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
from flask import Flask, jsonify


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


DATA = {
    "text": "Hello World!",
    "ok": True,
    "items": [
        "Hello",
        "World!",
    ],
}


@app.route("/")
def index():
    return jsonify(DATA)


@app.route("/v2")
def index_v2():
    return DATA


if __name__ == "__main__":
    app.run()
