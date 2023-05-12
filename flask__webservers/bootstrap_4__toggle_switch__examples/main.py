#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/twbs/bootstrap
# SOURCE: https://github.com/gitbrent/bootstrap4-toggle
# SOURCE: https://gitbrent.github.io/bootstrap4-toggle/


import logging
from flask import Flask, render_template


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
