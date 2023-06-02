#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from flask import Flask, render_template
from db import ProfileRating


app = Flask(__name__)


@app.route("/")
def index():
    items = ProfileRating.select().order_by(ProfileRating.id.desc())
    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.debug = True
    app.run(port=10017)
