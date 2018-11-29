#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pyautogui
pyautogui.FAILSAFE = False


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

    return jsonify({'text': 'ok'})


@app.route("/mouse_click", methods=['POST'])
def mouse_click():
    print('mouse_click')

    data = request.get_json()
    print('data:', data)

    possible_values = ('left', 'right')

    button = data.get('button')
    if button not in possible_values:
        text = f'Unsupported mouse button: {button}. Possible values: {", ".join(possible_values)}'
        print(text)
        return jsonify({'text': text})

    pyautogui.click(button=button)

    return jsonify({'text': 'ok'})


@app.route("/mouse_move", methods=['POST'])
def mouse_move():
    print('mouse_move')

    data = request.get_json()
    print('data:', data)

    relative_x = data['relative_x']
    relative_y = data['relative_y']

    pyautogui.moveRel(xOffset=relative_x, yOffset=relative_y)

    return jsonify({'text': 'ok'})


@app.route("/scroll", methods=['POST'])
def scroll():
    print('scroll')

    data = request.get_json()
    print('data:', data)

    down = data['down']

    value = -200 if down else 200
    pyautogui.scroll(value)

    return jsonify({'text': 'ok'})


if __name__ == "__main__":
    # Localhost
    app.debug = True
    app.run(
        # OR: host='127.0.0.1'
        # host='127.0.0.1',
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
