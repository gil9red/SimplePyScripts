#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from engineio.payload import Payload

from common import Task


DIR = Path(__file__).resolve().parent

Payload.max_decode_packets = 1000


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode=async_mode)


@app.route("/")
def index():
    return render_template(
        "index.html",
        title=DIR.name,
        commands=[
            "ping 127.0.0.1",
            "ping google.com",
            "python tests/return_code_999.py",
            "ipconfig",
        ],
    )


@socketio.on("run")
def run(message):
    def send_update_task(stdout: str = None, stderr: str = None):
        data = dict(
            id=task.id,
            command=task.command,
            status=task.status.name,
            process_id=task.process_id,
            process_return_code=task.process_return_code,
            stdout_add=stdout,
            stderr_add=stderr,
        )
        print("send_update_task", data)
        emit("update_task", data)

    def process_stdout(text: str):
        send_update_task(stdout=text)

    def process_stderr(text: str):
        send_update_task(stderr=text)

    task = Task(
        command=message["command"],
        stdout=process_stdout,
        stderr=process_stderr,
        encoding="cp866",
    )
    print(task)

    send_update_task()

    task.run(threaded=False)

    send_update_task()


if __name__ == "__main__":
    # Localhost
    HOST = "127.0.0.1"
    PORT = 5001

    app.debug = True
    socketio.run(
        app,
        host=HOST,
        port=PORT,
        allow_unsafe_werkzeug=True,
    )
