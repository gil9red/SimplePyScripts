#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/network', methods=['GET'])
def network():
    d = {
        'a': [1, 2, 3],
        'b': {
            'b1': [1],
            'b2': '2',
            'b3': 3,
        },
        'c': "CCC",
    }

    return jsonify(d)

if __name__ == "__main__":
    # Localhost
    app.run()

    # # Public IP
    # app.run(host='0.0.0.0')
