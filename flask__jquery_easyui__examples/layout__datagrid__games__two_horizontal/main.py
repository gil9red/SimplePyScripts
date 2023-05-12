#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://www.jeasyui.com/tutorial/index.php
# SOURCE: http://www.jeasyui.com/tutorial/app/crud.php


import logging
import sqlite3

from flask import Flask, render_template, jsonify, request


app = Flask(__name__, static_folder="../static")
logging.basicConfig(level=logging.DEBUG)


def create_connect(fields_as_dict=False):
    connect = sqlite3.connect("../datagrid__games/games.sqlite")

    if fields_as_dict:
        connect.row_factory = sqlite3.Row

    return connect


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_games", methods=["POST", "GET"])
def get_games():
    kind = request.args["kind"]

    with create_connect(fields_as_dict=True) as connect:
        sql = """
            SELECT id, name, price, append_date
            FROM game
            WHERE kind = ?
            ORDER BY name
        """
        items = list(map(dict, connect.execute(sql, (kind,)).fetchall()))

    return jsonify(items)


if __name__ == "__main__":
    # app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
