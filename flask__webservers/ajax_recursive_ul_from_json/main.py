#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import logging

from flask import Flask, jsonify, render_template


# SOURCE: https://ru.stackoverflow.com/questions/1364702/


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


DATA = [
    {
        "title": "Родитель 1",
        "url": "http://domain.com/url/"
    },
    {
        "title": "Родитель 2",
        "url": "http://domain.com/url2/",
        "children": [
            {
                "title": "Потомок 1",
                "url": "http://domain.com/url2/child1/"
            },
            {
                "title": "Потомок 2",
                "url": "http://domain.com/url2/child2/",
                "children": [
                    {
                        "title": "Потомок Потомка 1",
                        "url": "http://domain.com/url2/child1/child2/"
                    },
                    {
                        "title": "Потомок Потомка 2",
                        "url": "http://domain.com/url2/child1/child3/"
                    }
                ]
            }
        ]
    },
    {
        "title": "Родитель 3",
        "url": "http://domain.com/url3/"
    }
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/json/")
def get_json():
    return jsonify(DATA)


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
