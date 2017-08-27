#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return "Hello World!"


if __name__ == '__main__':
    app.debug = True
    app.threaded = True

    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
