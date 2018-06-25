#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pyautogui


# def scroll(down=True, value=200):
#     value = abs(value)
#
#     if down:
#         value = -value
#
#     pyautogui.scroll(value)
#
#
# scroll(down=True)
# scroll(down=True)
#
#
# quit()

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/key_click", methods=['POST'])
def key_click():
    print('key_click')

    data = request.get_json()
    print('data:', data)

    key = data['key']
    pyautogui.typewrite([key])

    return jsonify({'status': 'ok'})


if __name__ == "__main__":
    # Localhost
    app.debug = True
    app.run(
        # OR: host='127.0.0.1'
        host='192.168.0.102',
        port=9999,

        # # Включение поддержки множества подключений
        # threaded=True,
    )

    # # Public IP
    # app.run(
    #     host='0.0.0.0',
    #     port=9999,
    #
    #     # # Включение поддержки множества подключений
    #     # threaded=True,
    # )
