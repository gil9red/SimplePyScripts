#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, request
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=['POST'])
def index():
    data = request.data

    import binascii
    print(binascii.hexlify(data), data)

    return "Ok"


if __name__ == '__main__':
    app.debug = True

    app.run(
        port=33333,
        threaded=True,
    )
