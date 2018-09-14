#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://www.jeasyui.com/tutorial/index.php
# SOURCE: http://www.jeasyui.com/tutorial/app/crud.php


from flask import Flask, render_template, jsonify
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


import sqlite3


def create_connect(fields_as_dict=False):
    connect = sqlite3.connect('test_games.sqlite')

    if fields_as_dict:
        connect.row_factory = sqlite3.Row

    return connect


@app.route("/")
def index():
    return render_template("index.html")

# TODO: support addGame(), editGame(), deleteGame()


@app.route("/get_table", methods=['POST', 'GET'])
def get_table():
    with create_connect(fields_as_dict=True) as connect:
        get_game_sql = '''
            SELECT id, name, price, append_date
            FROM game
            ORDER BY name
        '''
        items = list(map(dict, connect.execute(get_game_sql).fetchall()))

    return jsonify(items)


if __name__ == '__main__':
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(
        port=5000,

        # :param threaded: should the process handle each request in a separate
        #                  thread?
        # :param processes: if greater than 1 then handle each request in a new process
        #                   up to this maximum number of concurrent processes.
        threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
