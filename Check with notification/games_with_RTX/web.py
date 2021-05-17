#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from db import Game

from flask import Flask, render_template_string
app = Flask(__name__)


@app.route('/')
def index():
    title = 'Games with RTX'
    URL = 'https://kanobu.ru/games/collections/igry-s-podderzhkoi-rtx/'
    headers = ['#', 'Игра', 'Дата добавления']
    games = Game.select().order_by(Game.id.desc())

    return render_template_string("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>{{ title }}</title>

    <style type="text/css">
        table {
            border-collapse: collapse; /* Убираем двойные линии между ячейками */
        }
            /* Увеличим заголовок таблиц */
            table > caption {
                font-size: 150%;
            }

            .frame th {
                font-size: 120%;
            }
            .frame td, .frame th {
                border: 1px double #333; /* Рамка таблицы */
                padding: 5px;
            }
            
        .thumbnail {
            width: 64px;
            height: 64px;
        }
    </style>
</head>
<body>   
    <table class="frame" style="width: 800px; margin:0 auto;">
        <caption><a href="{{ URL }}">{{ title }} ({{ games.count() }})</a></caption>
        <colgroup>
            <col span="1">
        </colgroup>
        <tbody>
            <tr>
            {% for header in headers %}
                <th>{{ header }}</th>
            {% endfor %}
            </tr>

        {% for game in games %}
            <tr>
                <td>{{ loop.index }}</td>
                <td valign="top">
                    <a target="_blank" href="{{ game.url }}">
                        <img class="thumbnail" src="{{ game.img_base64 }}" align="left">
                    </a>
                    <div>&nbsp;&nbsp;{{ game.name }}</div>
                </td>
                <td valign="top">{{ game.append_date }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
</body>
</html>
    """, games=games, headers=headers, title=title, URL=URL)


if __name__ == "__main__":
    app.debug = True

    # Localhost
    app.run(port=15555)

    # # Public IP
    # app.run(host='0.0.0.0')
