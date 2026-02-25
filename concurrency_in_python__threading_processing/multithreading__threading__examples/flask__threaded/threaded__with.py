#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import threading
from flask import Flask


app = Flask(__name__)


@app.route("/")
def index() -> str:
    return f"Current thread: {threading.current_thread()}"


if __name__ == "__main__":
    app.run(port=6000)
