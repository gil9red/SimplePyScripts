#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: Flask
# "Мега-Учебник Flask, Часть 1: Привет, Мир!": http://habrahabr.ru/post/193242/
# http://ru.wikibooks.org/wiki/Flask

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()