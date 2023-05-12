#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import re
import traceback

import requests

from bs4 import BeautifulSoup
from flask import Flask, render_template_string


def today_quotes(soup):
    # Узнаем количество сегодняшних цитат
    tag = soup.find(attrs=dict(id="stats"))

    match = re.search(r"сегодня (\d+),", tag.text)
    return int(match.group(1))


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    try:
        rs = requests.get("http://bash.im")
        soup = BeautifulSoup(rs.text, "lxml")

        number = today_quotes(soup)

        quotes = list()

        i = 0
        for quote in soup.find_all(attrs={"class": "quote"})[:number]:
            text = quote.find(attrs={"class": "text"})
            if text is None:
                continue

            i += 1
            print(i, text)
            quotes.append(text)

        return render_template_string(
            """\
        <html>
        <head><title>Новые за день цитаты bash.im</title></head>
        <body>

        {% if number %}
            <h1>Сегодня новых цитат: {{number}}</h1>

            {% for item in item_list %}
                <br><hr><br>
                {{ item }}
            {% endfor %}

            <br><hr><br>

        {% else %}
            <h1>Новых цитат нет</h1>
        {% endif %}

        </body>
        </html>""",
            number=number,
            item_list=quotes,
        )

    except BaseException as e:
        print("Error: {}\n\n{}".format(e, traceback.format_exc()))
        return "Error: " + str(e)


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
