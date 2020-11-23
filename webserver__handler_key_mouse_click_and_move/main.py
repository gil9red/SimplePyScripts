#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import threading
import time
import subprocess
import sys
import os.path
from pathlib import Path

import pyautogui
pyautogui.FAILSAFE = False

from flask import Flask, render_template, request, jsonify, send_from_directory
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


DIR = Path(__file__).resolve().parent


def show_cursor_as_target():
    # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/5e42dead5a522e1c128fb2fc611cca8a06986b4b/qt__pyqt__pyside__pyqode/show_target_icon__behind_cursor/main.py
    script_file_name = str(DIR.parent / 'qt__pyqt__pyside__pyqode/show_target_icon__behind_cursor\main.py')
    subprocess.Popen([sys.executable, script_file_name, '1000'])


def full_black_screen():
    # SOURCE: https://github.com/gil9red/SimplePyScripts/blob/69be0550dd64d3c40fe4f1851c6bce79fd582730/qt__pyqt__pyside__pyqode/full_black_screen.py
    script_file_name = str(DIR.parent / 'qt__pyqt__pyside__pyqode/full_black_screen.py')
    subprocess.Popen([sys.executable, script_file_name])


DATA = {
    "END_TIME": None,
    "DURATION": None,
}


def timer():
    while True:
        try:
            if not DATA["END_TIME"]:
                continue

            if DT.datetime.now() >= DATA["END_TIME"]:
                print('Timer activate! Press "space"')
                pyautogui.typewrite(['space'])
                DATA["END_TIME"] = None

        finally:
            time.sleep(1)


thread_timer = threading.Thread(target=timer)
thread_timer.start()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/set_timer", methods=['POST'])
def set_timer():
    print('set_timer')

    data = request.get_json()
    print('data:', data)

    secs = int(data['value']) if data['value'] else 0
    if secs:
        DATA["END_TIME"] = DT.datetime.now() + DT.timedelta(seconds=secs)
        DATA["DURATION"] = secs
    else:
        DATA["END_TIME"] = None
        DATA["DURATION"] = None

    return jsonify({'text': 'ok'})


@app.route("/get_timer", methods=['POST'])
def get_timer():
    # print('get_timer')

    now = DT.datetime.now()
    end_time = DATA["END_TIME"]
    
    secs = 0
    if end_time and end_time > now:
        secs = int((end_time - now).total_seconds())

    duration = DATA["DURATION"]
    if duration is None:
        duration = 0

    print(f'get_timer -> {secs} / {duration}')
    return jsonify({'value': secs, 'duration': duration})


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


@app.route("/show_cursor_as_target", methods=['POST'])
def on_show_cursor_as_target():
    print('show_cursor_as_target')

    show_cursor_as_target()

    return jsonify({'text': 'ok'})


@app.route("/full_black_screen", methods=['POST'])
def on_full_black_screen():
    print('full_black_screen')

    full_black_screen()

    return jsonify({'text': 'ok'})


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/icons'),
        'favicon.png'
    )


if __name__ == "__main__":
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=9999
    )
