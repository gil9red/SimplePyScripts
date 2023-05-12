#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import uuid

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode=async_mode)


@app.route("/")
def index():
    return render_template("index.html", async_mode=socketio.async_mode)


@socketio.on("my_event", namespace="/test")
def test_message(message):
    session["receive_count"] = session.get("receive_count", 0) + 1

    print(message)

    data = message["data"]

    if data == "CURRENT_DATE_TIME":
        response = DT.datetime.now().strftime("%Y-%m-%d_%H%M%S")

    elif data == "UUID":
        response = str(uuid.uuid4())

    elif data.startswith("CALC"):
        # TODO: don't use in production!
        response = str(eval(data[4:]))

    else:
        response = data

    emit(
        "my_response",
        {"data": response, "count": session["receive_count"]},
    )


@socketio.on("my_ping", namespace="/test")
def ping_pong():
    emit("my_pong")


@socketio.on("connect", namespace="/test")
def test_connect():
    emit("my_response", {"data": "Connected"})


@socketio.on("disconnect", namespace="/test")
def test_disconnect():
    print("Client disconnected", request.sid)


if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 12000
    print(f"http://{HOST}:{PORT}")

    socketio.run(
        app,
        host=HOST,
        port=PORT,
    )
