#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, render_template_string
app = Flask(__name__)


@app.route('/')
def index():
    from common import get_games
    cracked_games = get_games(filter_by_is_cracked=True, sorted_by_crack_date=True)
    not_cracked_games = get_games(filter_by_is_cracked=False, sorted_by_append_date=True)

    return render_template_string("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>Список взломанных игр</title>

    <style type="text/css">
        table {
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
        <caption><a href="https://en.wikipedia.org/wiki/Denuvo#List_of_games_using_Denuvo">Список взломанных игр</a></caption>

        <colgroup>
            <col span="1" style="width: 5%;">
        </colgroup>

        <tbody>
            <tr>
            {% for header in cracked_headers %}
                <th>{{ header }}</th>
            {% endfor %}
            </tr>

        {% for name, _, _, crack_date in cracked_games %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ name }}</td>
                <td>{{ crack_date }}</td>
                <td>
                    <button onclick="window.open('http://anti-tor.org/search/0/8/000/0/{{ name|replace('"', '')|replace("'", "") }}')">Rutor</button>
                    <button onclick="window.open('http://search.tfile.co/?q={{ name|replace('"', '')|replace("'", "") }}')">tFile</button>
                    <button onclick="window.open('http://www.torrentino.me/search?type=games&search={{ name|replace('"', '')|replace("'", "") }}')">Torrentino</button>
                    <button onclick="window.open('https://yandex.ru/yandsearch?text={{ name|replace('"', '')|replace("'", "") }}')">Yandex</button>
                    <button onclick="window.open('https://www.google.ru/#newwindow=1&q={{ name|replace('"', '')|replace("'", "") }}')">Google</button>
                </td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    
    <br><br>
    <hr>
    <br><br>
    
    <table>
        <caption>Еще не взломали:<caption>

        <colgroup>
            <col span="1" style="width: 5%;">
        </colgroup>

        <tbody>
            <tr>
            {% for header in not_cracked_headers %}
                <th>{{ header }}</th>
            {% endfor %}
            </tr>

        {% for name, _, append_date, _ in not_cracked_games %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ name }}</td>
                <td>{{ append_date }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
</body>
</html>
    """, cracked_headers=["№", "Название", "Дата взлома", "Поиск"], cracked_games=cracked_games,
         not_cracked_headers=["№", "Название", "Дата добавления"], not_cracked_games=not_cracked_games
    )


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
