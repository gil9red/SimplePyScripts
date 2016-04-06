#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, render_template_string
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)

import pyscreenshot as ImageGrab


@app.route("/")
def index():
    im = ImageGrab.grab()
    im.save('static/screenshot.png')

    return render_template_string('''\
    <html>
    <head><title>Show screenshot</title></head>
    <body>
    <p><img src="{{ url_for('static', filename='screenshot.png') }}" /></p>
    </body>
    </html>''')


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
