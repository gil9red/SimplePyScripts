#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from db import PeopleReached

from flask import Flask, render_template
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    items = PeopleReached.select().order_by(PeopleReached.id.desc())
    return render_template('index.html', people_reacheds=items)


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(
        port=10011,

        # :param threaded: should the process handle each request in a separate
        #                  thread?
        # :param processes: if greater than 1 then handle each request in a new process
        #                   up to this maximum number of concurrent processes.
        threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
