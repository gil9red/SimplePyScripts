#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging

from flask import Flask

# pip install flask-compress
from flask_compress import Compress


app = Flask(__name__)
Compress(app)

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return "Hello World!" * 100


if __name__ == "__main__":
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
