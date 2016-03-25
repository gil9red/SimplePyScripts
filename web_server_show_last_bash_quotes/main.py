#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, render_template_string
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    import requests
    rs = requests.get('http://bash.im')

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(rs.text, "lxml")

    quotes = list()

    i = 0
    for quote in soup.find_all(attrs={"class": "quote"}):
        text = quote.find(attrs={"class": "text"})
        if text is None:
            continue

        i += 1
        print(i, text)
        quotes.append(text)

    return render_template_string('''\
    <html>
    <head><title>Day last bash.im</title></head>
    <body>
    {% for item in item_list %}
       {{ item }}<br><hr><br>
    {% endfor %}
    </body>
    </html>''',
    item_list=quotes)


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
