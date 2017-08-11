#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, request, redirect
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)

import threading


def show(text):
    title = str(threading.current_thread())

    # Copy from: SimplePyScripts\windows__toast_balloontip_notifications\main.py
    from notifications import WindowsBalloonTip
    WindowsBalloonTip.balloon_tip(title, text, duration=20)


@app.route("/")
def index():
    return redirect('/show_notification?text=О, уведомление пришло!')


@app.route("/show_notification")
def show_notification():
    text = request.args.get('text')
    print('text:', text)

    thread = threading.Thread(target=show, args=(text,))
    thread.start()

    return 'Ok'


if __name__ == '__main__':
    # Localhost
    app.run(
        port=5000,
        threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
