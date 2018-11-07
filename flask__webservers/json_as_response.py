#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, jsonify
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return jsonify({
        'text': "Hello World!",
        'ok': True,
        'items': [
            'Hello',
            'World!',
        ]
    })


if __name__ == '__main__':
    app.run()
