#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import time

import requests

from flask import Flask


def go(port: int):
    app = Flask(__name__)

    logging.basicConfig(level=logging.DEBUG)

    @app.route("/")
    def index():
        return f"Hello World! (port={port})"

    app.run(port=port)


def go_parser(urls):
    while True:
        for url in urls:
            try:
                rs = requests.get(url)
                print('Parser: {}. "{}"'.format(rs, rs.text))

            except:
                pass

        time.sleep(2)


if __name__ == "__main__":
    # NOTE: recommended to add daemon=False or call join() for each process

    from multiprocessing import Process

    p1 = Process(target=go, args=(5001,))
    p1.start()

    p2 = Process(target=go, args=(5002,))
    p2.start()

    # OR:
    # for port in [5001, 5002]:
    #     p = Process(target=go, args=(port,))
    #     p.start()

    urls = ["http://127.0.0.1:5001/", "http://127.0.0.1:5002/"]
    p3 = Process(target=go_parser, args=(urls,))
    p3.start()

    # NOTE: optional
    # p1.join()
    # p2.join()
    # p3.join()
