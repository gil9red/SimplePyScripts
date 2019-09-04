#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/twbs/bootstrap
# SOURCE: https://github.com/twbs/bootstrap/releases
# SOURCE: https://www.w3schools.com/bootstrap4/bootstrap_utilities.asp


from flask import Flask, render_template
app = Flask(__name__, static_folder='../static')

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True

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
