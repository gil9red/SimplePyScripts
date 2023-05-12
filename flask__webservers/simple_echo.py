#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from flask import Flask, request, Response


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    print("-" * 20)
    print("Method:", request.method)
    print("Args:", dict(request.args))
    print("Data:", request.data)
    print("Form:", request.form)
    print("Headers:", dict(request.headers))
    print("-" * 20)
    return Response(
        response=request.data,
        content_type=request.headers.get("Content-Type"),
    )


if __name__ == "__main__":
    app.run(port=1000)
