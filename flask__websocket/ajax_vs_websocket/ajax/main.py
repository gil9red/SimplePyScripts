#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from timeit import default_timer
from threading import Lock

from flask import Flask, render_template, request, jsonify


app = Flask(__name__, static_folder="../_static")
app.config["SECRET_KEY"] = "secret!"

lock = Lock()
DATA = {
    "count": 0,
    "start_time": 0.0,
}


@app.route("/")
def index():
    with lock:
        DATA["count"] = 0

    return render_template("index.html")


@app.route("/post_method", methods=["POST"])
def post_method():
    data = request.get_json()
    # print(data)

    with lock:
        if DATA["count"] == 0:
            DATA["start_time"] = default_timer()

        DATA["count"] += 1

    return jsonify({
        "number": data["number"],
        "count": DATA["count"],
        "elapsed": round(default_timer() - DATA["start_time"], 3),
    })


if __name__ == "__main__":
    # Localhost
    HOST = "127.0.0.1"
    PORT = 12000
    print(f"http://{HOST}:{PORT}")

    app.debug = True
    app.run(host=HOST, port=PORT)
