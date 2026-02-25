#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import binascii
import logging

from flask import Flask, request


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=["POST"])
def index() -> str:
    data = request.data
    print(binascii.hexlify(data), data)

    return "Ok"


if __name__ == "__main__":
    app.debug = True

    app.run(port=33333)
