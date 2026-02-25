#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SOURCE: https://stackoverflow.com/a/5089963/5909792


import socket
from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def hello() -> str:
    return "Hello, world! running on %s" % request.host


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    print("sock.getsockname:", sock.getsockname())

    sock.close()
    app.run(port=port)
