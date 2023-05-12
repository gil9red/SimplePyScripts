#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://www.jeasyui.com/tutorial/index.php
# SOURCE: http://www.jeasyui.com/tutorial/app/crud.php


import datetime as DT
import logging
import sqlite3

from flask import Flask, render_template, jsonify, request


app = Flask(__name__, static_folder="../static")
logging.basicConfig(level=logging.DEBUG)


def create_connect(fields_as_dict=False):
    connect = sqlite3.connect("games.sqlite")

    if fields_as_dict:
        connect.row_factory = sqlite3.Row

    return connect


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_games", methods=["POST", "GET"])
def get_games():
    with create_connect(fields_as_dict=True) as connect:
        sql = """
            SELECT id, name, price, append_date
            FROM game
            ORDER BY name
        """
        items = list(map(dict, connect.execute(sql).fetchall()))

    return jsonify(items)


@app.route("/save_game", methods=["POST", "GET"])
def save_game():
    try:
        name = request.form["name"]
        price = request.form["price"]

        # 2017-06-03 21:21:17
        append_date = DT.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with create_connect() as connect:
            sql = "INSERT INTO Game (name, price, append_date) VALUES (?,?,?)"
            # rs = connect.execute(sql, (name, price, append_date))
            connect.execute(sql, (name, price, append_date))

    except Exception as e:
        return jsonify({"errorMsg": f'Some errors occured: "{e}"'})

    return jsonify({"success": True})
    # return jsonify({
    #     'id': rs.lastrowid,
    #     'name': name,
    #     'price': price,
    #     'append_date': append_date
    # })


@app.route("/update_game", methods=["POST", "GET"])
def update_game():
    try:
        id_ = request.args["id"]
        name = request.form["name"]
        price = request.form["price"]

        with create_connect() as connect:
            sql = "UPDATE Game SET name = ?, price = ? WHERE id = ?"
            connect.execute(sql, (name, price, id_))

    except Exception as e:
        return jsonify({"errorMsg": f'Some errors occured: "{e}"'})

    return jsonify({"success": True})


@app.route("/delete_game", methods=["POST", "GET"])
def delete_game():
    try:
        id_ = request.form["id"]

        with create_connect() as connect:
            sql = "DELETE FROM Game WHERE id = ?"
            connect.execute(sql, (id_,))

    except Exception as e:
        return jsonify({"errorMsg": f'Some errors occured: "{e}"'})

    return jsonify({"success": True})


# TODO: диалог редактирования кнопку Ок показывает активной только если данные изменены


if __name__ == "__main__":
    # app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
