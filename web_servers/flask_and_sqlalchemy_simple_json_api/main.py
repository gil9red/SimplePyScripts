#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, request, render_template_string, render_template
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template_string("Hello")


@app.route("/api/v1/get")
def api_v1_get():
    _id = request.args.get('id', None)
    return "id='{}', '{}'".format(_id)


@app.route("/api/v1/search")
def api_v1_search():
    _id = request.args.get('id', None)
    return "id='{}', '{}'".format(_id)


@app.route("/api/v1/post", methods=['GET', 'POST'])
def api_v1_post():
    _id = request.args.get('id', None)
    return "id='{}', '{}'".format(_id)


@app.route("/all-links")
def all_links():
    links = []

    for rule in app.url_map.iter_rules():
        try:
            from flask import url_for
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if url.startswith('/api'):
                links.append(url)
        except:
            pass

    return render_template("all_api_links.html", links=links)


if __name__ == '__main__':
    # Localhost
    app.debug = True
    app.run()

