#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, render_template_string
app = Flask(__name__)


@app.route('/')
def index():
    from common import get_games
    games = get_games(filter_by_is_cracked=True)

    return render_template_string("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>Список взломанных игр</title>

    <style type="text/css">
        table {
            width: 40%;
            border-collapse: collapse; /* Убираем двойные линии между ячейками */
        }
            /* Увеличим заголовок таблиц */
            table > caption {
                font-size: 150%;
            }

            th {
                font-size: 120%;
            }
            td, th {
                border: 1px double #333; /* Рамка таблицы */
                padding: 5px;
            }
    </style>
</head>
<body>
    <table>
        <colgroup>
            <col span="1" style="width: 5%;">
            <col span="1" style="width: 70%;">
            <col span="1" style="width: 20%;">
        </colgroup>

        <tbody>
            <tr>
            {% for header in headers %}
                <th>{{ header }}</th>
            {% endfor %}
            </tr>

        {% for name in games %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ name }}</td>
                <td></td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
</body>
</html>
    """, games=[name for name, _ in games], headers=["№", "Название", "Поиск"])


if __name__ == "__main__":
    app.debug = True

    # Localhost
    app.run(
        # Включение поддержки множества подключений
        threaded=True,
        port=5555,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
