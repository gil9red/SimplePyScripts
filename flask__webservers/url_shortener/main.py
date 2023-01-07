#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path
from urllib.parse import urlparse, urljoin

from flask import Flask, request, render_template, redirect, abort, jsonify

import db


app = Flask(__name__)


def server_url() -> str:
    parse = urlparse(request.url)
    return '{}://{}/'.format(parse.scheme, parse.netloc)


@app.route("/", defaults={'link_id': ''})
@app.route("/<path:link_id>")
def index(link_id: str):
    if link_id:
        link = db.Link.get_by_link_id(link_id)
        if not link:
            abort(404)

        url = link.link_url
        return redirect(url)

    return render_template(
        'index.html',
        title=Path(__file__).parent.resolve().stem
    )


@app.route("/add", methods=['POST'])
def add():
    result = {
        "url": "",
    }
    if 'url' in request.form:
        link_url = request.form['url']
        link = db.Link.add(link_url)
        result['url'] = urljoin(server_url(), link.link_id)

    return jsonify(result)


if __name__ == '__main__':
    # # Localhost
    # app.run(port=5001)

    # Public IP
    app.run(host='0.0.0.0')
