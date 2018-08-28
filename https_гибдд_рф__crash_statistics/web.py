#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, render_template_string
from common import get_crash_statistics_list_db


app = Flask(__name__)


@app.route('/')
def index():
    headers = ["№", "Дата", "ДТП", "Погибли", "Погибло детей", "Ранены", "Ранено детей"]
    rows = get_crash_statistics_list_db()

    return render_template_string("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>{{ title }}</title>

    <style type="text/css">
        /* Для размещения таблицы по центру. SOURCE: https://stackoverflow.com/a/9402889/5909792 */
        html, body {
            width: 100%;
        }
    
        table {
            border-collapse: collapse; /* Убираем двойные линии между ячейками */
            width: 50%; /* Ширина таблицы */
            
            /* Для размещения таблицы по центру. SOURCE: https://stackoverflow.com/a/9402889/5909792 */
            margin: 0 auto;
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
        <caption>{{ title }}</caption>

        <colgroup>
            <col span="1" style="width: 5%;">
        </colgroup>

        <tbody>
            <tr>
            {% for header in headers %}
                <th>{{ header }}</th>
            {% endfor %}
            </tr>

        {% for row in rows %}
            <tr>
                <td>{{ loop.index }}</td>
                
                {% for value in row %}
                <td>{{ value }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
        </tbody>
    </table>
</body>
</html>
    """, title="АВАРИЙНОСТЬ НА ДОРОГАХ РОССИИ", headers=headers, rows=rows)


if __name__ == "__main__":
    app.debug = True

    # Localhost
    app.run(
        # Включение поддержки множества подключений
        threaded=True,
        port=10009,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
