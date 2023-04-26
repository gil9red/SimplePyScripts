#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import threading

from flask import Flask


def run(port: int = 80):
    app = Flask(__name__)
    logging.basicConfig(level=logging.DEBUG)

    @app.route("/")
    def index():
        html = "Hello World! (port={})".format(port)
        print(html)

        return html

    app.run(port=port)


if __name__ == "__main__":
    # NOTE: recommended to add daemon=False or call join() for each thread

    thread = threading.Thread(target=run, args=(5000,))
    thread.start()

    thread = threading.Thread(target=run, args=(5001,))
    thread.start()

    thread = threading.Thread(target=run, args=(5002,))
    thread.start()

    # OR:
    # for port in [5000, 5001, 5002]:
    #     thread = threading.Thread(target=run, args=(port,))
    #     thread.start()
