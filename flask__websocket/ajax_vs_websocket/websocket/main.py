#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from timeit import default_timer
from threading import Lock

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from engineio.payload import Payload


Payload.max_decode_packets = 1000


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__, static_folder="../_static")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode=async_mode)

lock = Lock()
DATA = {
    "count": 0,
    "start_time": 0.0,
}


@app.route("/")
def index():
    with lock:
        DATA["count"] = 0

    return render_template("index.html", async_mode=socketio.async_mode)


@socketio.on("post_method", namespace="/test")
def post_method(message):
    # print(message)

    with lock:
        if DATA["count"] == 0:
            DATA["start_time"] = default_timer()

        DATA["count"] += 1

    emit(
        "my_response",
        {
            "number": message["number"],
            "count": DATA["count"],
            "elapsed": round(default_timer() - DATA["start_time"], 3),
        },
    )


if __name__ == "__main__":
    # Localhost
    HOST = "127.0.0.1"
    PORT = 12001
    print(f"http://{HOST}:{PORT}")

    app.debug = True
    socketio.run(
        app,
        host=HOST,
        port=PORT,
    )
