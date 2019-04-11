#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from threading import Thread
import time

from flask import Flask
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


text = "Hello World!"


def go():
    time.sleep(2)
    print('\n')

    global text

    while True:
        text = input(f'Current text is "{text}". New next: ')


@app.route("/")
def index():
    return text


if __name__ == '__main__':
    thread = Thread(target=go)
    thread.start()

    # app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(
        port=5000,

        # :param threaded: should the process handle each request in a separate
        #                  thread?
        # :param processes: if greater than 1 then handle each request in a new process
        #                   up to this maximum number of concurrent processes.
        threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
