#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://flask.palletsprojects.com/en/3.0.x/errorhandling/


import logging

from flask import Flask, render_template
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("errors/500.html", e=e), 500


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/500")
def do_500():
    1/0


if __name__ == "__main__":
    app.run(port=5000)
