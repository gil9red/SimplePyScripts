#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, request
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    user_agent = request.headers['User-Agent']
    print(user_agent)

    return f"""\
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
        <div>{user_agent}</div>
    </body>
</html>
"""


if __name__ == '__main__':
    app.run()
