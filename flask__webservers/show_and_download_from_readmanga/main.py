#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import os
import sys

from flask import Flask, render_template_string, request, redirect


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Добавление пути основной папки репозитория, чтобы импортировать модуль download_volume_readmanga
dir = os.path.dirname(__file__)
dir = os.path.dirname(dir)
dir = os.path.dirname(dir)
sys.path.append(dir)
from download_volume_readmanga import get_url_images, save_urls_to_zip


NOT_ARGS_HTML = """\
<h1>К url нужно добавить параметр url: адрес главы.</h1>
<h2>Например: <a href="{0}">{0}</a></h2>
"""

DEFAULT_URL_MANGA = "https://readmanga.live/one_punch_man__A1bc88e/vol1/1"


# TODO: FIXED HTTP STATUS "402 Payment Required" on <img src="..."/>
#       Как вариант, можно скачивать картинки в папку сервера и отображать их из него
@app.route("/")
def index():
    if not request.args:
        return NOT_ARGS_HTML.format(f"/?url={DEFAULT_URL_MANGA}")

    url = request.args.get("url")
    print("Url manga:", url)

    images_urls = get_url_images(url)
    print("Urls images:", images_urls)

    return render_template_string(
        """\
    <html>
    <head><title>Показать и скачать из readmanga</title></head>
    <body>

    <p>Манга: <a href="{{ url }}"> {{ url }} </a></h2></p>
    <p><a href="/export?url={{ url }}">Скачать как zip архив</a></p>
    <br>
    <hr>
    <br>

    {% for item in images_urls %}
        <p><img src="{{ item }}" /></p>
        <br>
    {% endfor %}

    </body>
    </html>
    """,
        url=url,
        images_urls=images_urls,
    )


@app.route("/export")
def export():
    if not request.args:
        return NOT_ARGS_HTML.format(f"/export?{DEFAULT_URL_MANGA}")

    url = request.args.get("url")
    print("Url manga:", url)

    file_name = os.path.basename(url) + ".zip"
    static_file_name = os.path.join("static", file_name)

    # Если архива с главой нет, качаем ее
    if not os.path.exists(static_file_name):
        print(f'Архива "{static_file_name}" нет, качаем и создаем.')

        images_urls = get_url_images(url)
        print("Urls images:", images_urls)

        save_urls_to_zip(static_file_name, images_urls)
        print("Сохранено в архиве:", file_name)

    # Перенаправляем к url с архивом
    relative_url = render_template_string(
        "{{ url_for('static', filename='%s') }}" % (file_name,)
    )
    return redirect(relative_url)


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
