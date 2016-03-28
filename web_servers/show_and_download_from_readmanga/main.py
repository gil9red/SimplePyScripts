#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, render_template_string, request
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)

# Добавление пути основной папки репозитория, чтобы импортировать модуль download_volume_readmanga
import os
dir = os.path.dirname(__file__)
dir = os.path.dirname(dir)
dir = os.path.dirname(dir)

import sys
sys.path.append(dir)

from download_volume_readmanga import get_url_images


# TODO: добавить возможность скачать главы в архиве


@app.route("/")
def index():
    if not request.args:
        return """\
        <h1>К url нужно добавить параметр url -- адрес главы.</h1>
        <h2>Например: <a href="{0}">{0}</a></h2>
        """.format('http://127.0.0.1:5001/?url=http://readmanga.me/one__piece/vol60/591')

    url = request.args.get('url')
    print('Url manga:', url)

    images_urls = get_url_images(url)
    print('Urls images:', images_urls)

    return render_template_string('''\
    <html>
    <head><title>Показать и скачать из readmanga</title></head>
    <body>

    <p>Манга: <a href="{{ url }}"> {{ url }} </a></h2></p>
    <br>
    <hr>
    <br>

    {% for item in images_urls %}
        <p><img src="{{ item }}" /></p>
        <br>
    {% endfor %}

    </body>
    </html>
    ''', url=url, images_urls=images_urls)


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
