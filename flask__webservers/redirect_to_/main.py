#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
from flask import Flask, redirect, request, render_template_string


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string(
        """\
<a href="{{ example }}">{{ example }}</a><br><br>
    
<form action="/redirect">
    <input type="url" name="url" value="http://bash.im/">
    <input type="submit" value="Перейти">
<form>
    """,
        example="/redirect?url=http://bash.im/",
    )


@app.route("/redirect")
def redirect_to():
    # From url arguments
    url = request.args.get("url", None)
    if not url:
        # From form arguments
        url = request.form.get("url", "/")

    return redirect(url)


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
