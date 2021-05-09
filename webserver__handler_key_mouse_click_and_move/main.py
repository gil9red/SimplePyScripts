#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import base64
import datetime as DT
import logging
import time
import subprocess
import sys
import os.path

from pathlib import Path
from threading import Thread
from multiprocessing import Process

import pyautogui

import requests
from requests.exceptions import ConnectionError

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from engineio.payload import Payload


Payload.max_decode_packets = 1000

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

DIR = Path(__file__).resolve().parent

PORT_REMOTE_SCREENSHOT = 19999
URL_REMOTE_SCREENSHOT = 'http://127.0.0.1:%s/command/{}' % PORT_REMOTE_SCREENSHOT


def run_frameless_widget_with_webserver():
    # Запуск виджета-рамки для передачи скриншотов, по умолчанию скрыт
    Process(
        target=frameless_widget_with_webserver.main,
        args=(PORT_REMOTE_SCREENSHOT, DATA["STREAM_MODE"])
    ).start()


def send_command_frameless_widget_with_webserver(command: str) -> requests.Response:
    url = URL_REMOTE_SCREENSHOT.format(command)

    # Попробуем отправить команду и если окно закрыто, переоткрыть его
    try:
        rs = requests.post(url)
    except ConnectionError:
        run_frameless_widget_with_webserver()
        rs = requests.post(url)

    return rs


pyautogui.FAILSAFE = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


# Для импорта frameless_widget_with_webserver
sys.path.append(r'..\qt__pyqt__pyside__pyqode\remote_controller__widget_with_webserver')
import frameless_widget_with_webserver


def get_img_base64(data: bytes) -> str:
    img_base64 = base64.standard_b64encode(data).decode('utf-8')
    return "data:image/png;base64," + img_base64


def get_logger(name=__file__):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(message)s')

    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


log = get_logger()


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
    "STREAM_MODE": False,
}


def send_about_timer(secs, duration):
    if duration is None:
        duration = 0

    socketio.emit(
        'about_timer',
        {'value': secs, 'duration': duration},
        broadcast=True,
    )
    # log.info(f'get_timer -> {secs} / {duration}')


def get_secs() -> int:
    if not DATA["END_TIME"]:
        return 0

    now = DT.datetime.now()
    end_time = DATA["END_TIME"]

    secs = 0
    if end_time and end_time > now:
        secs = int((end_time - now).total_seconds())

    return secs


def timer():
    while True:
        try:
            if not DATA["END_TIME"]:
                continue

            if DT.datetime.now() >= DATA["END_TIME"]:
                log.info('Timer activate! Press "space"')
                pyautogui.typewrite(['space'])
                DATA["END_TIME"] = None
                continue

            send_about_timer(get_secs(), DATA["DURATION"])

        finally:
            time.sleep(1)


thread_timer = Thread(target=timer)
thread_timer.start()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/set_timer", methods=['POST'])
def set_timer():
    log.info('set_timer')

    data = request.get_json()
    log.info(f'data: {data}')

    secs = int(data['value']) if data['value'] else 0
    if secs:
        DATA["END_TIME"] = DT.datetime.now() + DT.timedelta(seconds=secs)
        DATA["DURATION"] = secs
    else:
        DATA["END_TIME"] = None
        DATA["DURATION"] = None

    # Понадобится, например, при отмене таймера
    send_about_timer(secs, DATA["DURATION"])

    return jsonify({'text': 'ok'})


@socketio.on('connect')
def on_connect():
    user_agent = request.headers.get('User-Agent')

    secs = get_secs()
    duration = DATA["DURATION"]

    log.info(f'on_connect: {user_agent}\n    secs: {secs}, duration: {duration}')
    send_about_timer(secs, duration)


@app.route("/key_click", methods=['POST'])
def key_click():
    log.info('key_click')

    data = request.get_json()
    log.info(f'data: {data}')

    key = data['key']

    # Если включен режим, то перемещаться будет курсор мышки
    # Кнопками удобнее точно целиться курсором мышки
    if DATA["STREAM_MODE"]:
        relative_x = relative_y = 0

        if key == 'up':
            relative_y = -5
        elif key == 'down':
            relative_y = 5
        elif key == 'left':
            relative_x = -5
        elif key == 'right':
            relative_x = 5

        pyautogui.moveRel(xOffset=relative_x, yOffset=relative_y)

    else:
        pyautogui.typewrite([key])

    return jsonify({'text': 'ok'})


@app.route("/mouse_click", methods=['POST'])
def mouse_click():
    log.info('mouse_click')

    data = request.get_json()
    log.info(f'data: {data}')

    possible_values = ('left', 'right')

    button = data.get('button')
    if button not in possible_values:
        text = f'Unsupported mouse button: {button}. Possible values: {", ".join(possible_values)}'
        log.info(text)
        return jsonify({'text': text})

    pyautogui.click(button=button)

    return jsonify({'text': 'ok'})


@app.route("/mouse_move", methods=['POST'])
def mouse_move():
    log.info('mouse_move')

    data = request.get_json()
    log.info(f'data: {data}')

    relative_x = data['relative_x']
    relative_y = data['relative_y']

    pyautogui.moveRel(xOffset=relative_x, yOffset=relative_y)

    # Если включен режим, то вместе с курсором перемещаться будет окно-рамка
    if DATA["STREAM_MODE"]:
        send_command_frameless_widget_with_webserver('MOVE_TO_CURSOR')

    return jsonify({'text': 'ok'})


@app.route("/scroll", methods=['POST'])
def scroll():
    log.info('scroll')

    data = request.get_json()
    log.info(f'data: {data}')

    down = data['down']

    value = -200 if down else 200
    pyautogui.scroll(value)

    return jsonify({'text': 'ok'})


@app.route("/set_stream_mode", methods=['POST'])
def set_stream_mode():
    log.info('set_stream_mode')

    data = request.get_json()
    log.info(f'data: {data}')

    value = data['value']
    DATA["STREAM_MODE"] = value

    command = 'SHOW' if value else 'HIDE'
    send_command_frameless_widget_with_webserver(command)
    if command == 'SHOW':
        send_command_frameless_widget_with_webserver('MOVE_TO_CURSOR')

    return jsonify({'text': 'ok'})


@app.route("/get_screenshot", methods=['POST'])
def get_screenshot():
    log.info('get_screenshot')

    data = request.get_json()
    log.info(f'data: {data}')

    rs = send_command_frameless_widget_with_webserver("SCREENSHOT")

    return jsonify({
        'time': int(time.time()),
        'img_base64': get_img_base64(rs.content)
    })


@app.route("/show_cursor_as_target", methods=['POST'])
def on_show_cursor_as_target():
    log.info('show_cursor_as_target')

    show_cursor_as_target()

    return jsonify({'text': 'ok'})


@app.route("/full_black_screen", methods=['POST'])
def on_full_black_screen():
    log.info('full_black_screen')

    full_black_screen()

    return jsonify({'text': 'ok'})


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/icons'),
        'favicon.png'
    )


if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 9999

    run_frameless_widget_with_webserver()

    # TODO: вебсокеты почему то не работают при app.debug = True
    # app.debug = True
    # if app.debug:
    #     logging.basicConfig(level=logging.DEBUG)

    # logging.basicConfig(level=logging.DEBUG)

    log.info(f'HTTP server running on http://{"127.0.0.1" if HOST == "0.0.0.0" else HOST}:{PORT}')

    socketio.run(
        app,
        host=HOST,
        port=PORT
    )
