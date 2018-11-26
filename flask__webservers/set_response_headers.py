#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, Response
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    rs = Response("Hello World!")
    rs.headers['User-Agent'] = "FooBar"

    return rs


if __name__ == '__main__':
    app.run()
