#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
from flask import Flask, request


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    user_agent = request.headers["User-Agent"]
    print(user_agent)

    return user_agent


if __name__ == "__main__":
    app.run()
