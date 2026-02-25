#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install flask==2.3.3
from flask import Flask

# pip install flask-cors==4.0.0
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/")
def index() -> str:
    return "Hello World!"


if __name__ == "__main__":
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=50000)

    # # Public IP
    # app.run(host='0.0.0.0')
