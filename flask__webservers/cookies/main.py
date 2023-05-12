#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
from flask import Flask, request, make_response, jsonify


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/get-cookies")
def get_cookies():
    return jsonify(request.cookies)


@app.route("/set-cookies", methods=["POST"])
def set_cookies():
    rs = make_response(jsonify(dict(ok=True)))

    for k, v in request.args.items():
        rs.set_cookie(k, v)

    return rs


if __name__ == "__main__":
    app.debug = True
    app.run(
        port=5001,
    )
