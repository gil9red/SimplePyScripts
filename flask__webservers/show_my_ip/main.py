#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
from flask import Flask, request


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index() -> str:
    return f"""Your IPv4 Address Is: {request.remote_addr}"""


if __name__ == "__main__":
    # # Localhost
    # app.run(port=5001)

    # Public IP
    app.run(host="0.0.0.0")
