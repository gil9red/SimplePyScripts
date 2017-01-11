#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, render_template_string
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    from common import DB_FILE_NAME, FINISHED, FINISHED_WATCHED

    import sqlite3
    conn = sqlite3.connect(DB_FILE_NAME)
    c = conn.cursor()

    get_game_sql = 'SELECT name, price, modify_date FROM game where kind = ? order by name'
    finished_games = c.execute(get_game_sql, (FINISHED,)).fetchall()
    finished_watched_games = c.execute(get_game_sql, (FINISHED_WATCHED,)).fetchall()

    headers = ['NAME', 'PRICE', 'MODIFY_DATE']

    return render_template_string('''\
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Список игр</title>

    <style type="text/css">
        table > caption {
            font-size: 150%;
        }
    </style>
</head>
<body>
     <table width="70%" border="1">
        <caption>Пройденные игры</caption>
        <tr>
        {% for header in headers %}
            <th>{{ header }}</th>
        {% endfor %}
        </tr>

        {% for values in finished_games %}
            <tr>
            {% for value in values %}
                <td>{{ value }}</td>
            {% endfor %}
            </tr>
        {% endfor %}
     </table>
     <br><br><br>

     <table width="70%" border="1">
        <caption>Просмотренные игры</caption>
        <tr>
        {% for header in headers %}
            <th>{{ header }}</th>
        {% endfor %}
        </tr>

        {% for values in finished_watched_games %}
            <tr>
            {% for value in values %}
                <td>{{ value }}</td>
            {% endfor %}
            </tr>
        {% endfor %}
     </table>
</body>
</html>
''', headers=headers, finished_games=finished_games, finished_watched_games=finished_watched_games)


if __name__ == '__main__':
    # Localhost
    app.debug = True

    app.run(
        port=5000,

        # Включение поддержки множества подключений
        threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')

