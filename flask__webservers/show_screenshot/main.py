#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging

from flask import Flask, render_template_string

import pyscreenshot as ImageGrab


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    img = ImageGrab.grab()
    img.save("static/screenshot.png")

    return render_template_string(
        """\
    <html>
    <head><title>Show screenshot</title></head>
    <body>
    <p><img src="{{ url_for('static', filename='screenshot.png') }}" /></p>
    </body>
    </html>"""
    )


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
