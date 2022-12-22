#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging

from flask import Flask, render_template
from db import ProfileRating


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    items = ProfileRating.select().order_by(ProfileRating.id.desc())
    return render_template('index.html', items=items)


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=10017)

    # # Public IP
    # app.run(host='0.0.0.0')
