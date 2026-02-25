#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from datetime import datetime
from threading import Thread

from flask import Flask, render_template, session, request

# pip install flask-socketio==5.3.6
from flask_socketio import SocketIO, emit


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode=async_mode)


def send_all_cycled() -> None:
    with app.app_context():
        i = 0
        while True:
            i += 1
            emit(
                "my_response_all",
                {"data": f"#{i}. {datetime.now().isoformat()}"},
                broadcast=True,  # Send all clients
                namespace="/",
            )
            time.sleep(1)


thread = Thread(target=send_all_cycled)
thread.daemon = True
thread.start()


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("my_event")
def test_message(message) -> None:
    session["receive_count"] = session.get("receive_count", 0) + 1
    print(message)

    response = message["data"]
    emit(
        "my_response",
        {"data": response, "count": session["receive_count"], "sid": request.sid},
        broadcast=True,  # Send all clients
    )


@socketio.on("my_ping")
def ping_pong() -> None:
    emit("my_pong")


@socketio.on("connect")
def test_connect() -> None:
    print("Client connected", request.sid)
    emit("my_response", {"data": f"Connected!", "count": 0, "sid": request.sid})


@socketio.on("disconnect")
def test_disconnect() -> None:
    print("Client disconnected", request.sid)


if __name__ == "__main__":
    # HOST = '127.0.0.1'
    # HOST = "0.0.0.0"
    PORT = 12000
    # print(f"http://{HOST}:{PORT}")

    socketio.run(
        app,
        # host=HOST,
        port=PORT,
        allow_unsafe_werkzeug=True,
    )
