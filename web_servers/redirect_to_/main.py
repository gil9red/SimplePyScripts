#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, redirect, request, render_template_string
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string('''
<form action="/redirect">
    <input type="text" name="url" value="http://bash.im/">
    <input type="submit" value="Перейти">
<form>
    ''')


@app.route('/redirect')
def redirect_to():
    # From url arguments
    url = request.args.get('url', None)
    if not url:
        # From form arguments
        url = request.form.get('url', '/')

    return redirect(url)


if __name__ == '__main__':
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
