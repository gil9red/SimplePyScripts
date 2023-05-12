#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import os
import sys

from flask import Flask, render_template_string, request, redirect


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Добавление пути основной папки репозитория, чтобы импортировать модуль random_abusive
dir = os.path.dirname(__file__)
dir = os.path.dirname(dir)
dir = os.path.dirname(dir)
sys.path.append(dir)
import random_abusive


@app.route("/")
def index():
    if not request.args:
        return redirect("/?number=10&chain=2")

    print("query_string:", request.query_string)
    number = int(request.args["number"])
    chain = int(request.args["chain"])

    words = random_abusive.get_words(number, chain)
    print("words:", words)

    return render_template_string(
        """\
    <html>
    <head><title>Рандомные матерные слова</title></head>
    <body>
    {% for word in words %}
        <p>{{ word }}</p>
    {% endfor %}

    </body>
    </html>
    """,
        words=words,
    )


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
