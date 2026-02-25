#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import threading
import sys

from pathlib import Path

from flask import Flask, request, redirect

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(
    str(ROOT / "winapi__windows__ctypes/windows__toast_balloontip_notifications")
)
from run_notify import run_in_thread


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


def show(text) -> None:
    title = str(threading.current_thread())
    run_in_thread(title, text, duration=20)


@app.route("/")
def index():
    return redirect("/show_notification?text=О, уведомление пришло!")


@app.route("/show_notification")
def show_notification() -> str:
    text = request.args.get("text")
    print("text:", text)

    # Run function in new thread
    thread = threading.Thread(target=show, args=(text,))
    thread.start()

    return "Ok"


if __name__ == "__main__":
    # Localhost
    app.run(
        port=5000,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
