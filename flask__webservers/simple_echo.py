#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, request, Response
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    print('-' * 20)
    print(request.data)
    print(dict(request.headers))
    print('-' * 20)
    return Response(
        response=request.data,
        content_type=request.headers['Content-Type']
    )


if __name__ == "__main__":
    app.run(port=1000)
