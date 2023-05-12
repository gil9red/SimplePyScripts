#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import os
import subprocess

from pathlib import Path

from flask import Flask, jsonify, render_template


DIR = Path(__file__).resolve().parent
DIR_BAT_SCRIPTS = DIR / "bat_scripts"


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template(
        "index.html",
        scripts=[f.name for f in DIR_BAT_SCRIPTS.glob("*.bat")],
    )


@app.route("/os_startfile/<path:script_name>", methods=["POST"])
def on_os_startfile(script_name: str):
    os.startfile(DIR_BAT_SCRIPTS / script_name)
    return jsonify({"ok": True})


@app.route("/subprocess/<path:script_name>", methods=["POST"])
def on_subprocess(script_name: str):
    result = subprocess.check_output(
        DIR_BAT_SCRIPTS / script_name, universal_newlines=True, timeout=1
    )
    print(result)
    os.startfile(DIR_BAT_SCRIPTS / script_name)
    return jsonify({"ok": True, "result": result})


if __name__ == "__main__":
    app.debug = True

    # Localhost
    # port=0 - random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
