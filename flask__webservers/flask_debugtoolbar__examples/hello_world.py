#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config["SECRET_KEY"] = "<replace with a secret key>"


@app.route("/")
def index() -> str:
    # NOTE: Need tab body: "Could not insert debug toolbar. </body> tag not found in response."
    return "<body>Hello World!</body>"


if __name__ == "__main__":
    app.debug = True

    if app.debug:
        logging.basicConfig(level=logging.DEBUG)

    toolbar = DebugToolbarExtension(app)

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
