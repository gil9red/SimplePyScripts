#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT

from flask import Flask, render_template_string
app = Flask(__name__)

from common import get_games


@app.route('/')
def index():
    cracked_games = get_games(filter_by_is_cracked=True, sorted_by_crack_date=True)

    not_cracked_games = []

    for name, _, _, _, release_date_str in get_games(filter_by_is_cracked=False, sorted_by_append_date=True):
        try:
            release_date = DT.datetime.strptime(release_date_str, '%d/%m/%Y').date()
            days_passed = (DT.date.today() - release_date).days
        except:
            days_passed = '-'

        not_cracked_games.append((name, release_date_str, days_passed))

    return render_template_string("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>Denuvo. Список взломанных игр</title>

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
    </style>
</head>
<body>
    <script>
        function openWindowWithPost(url, data) {
            var form = document.createElement("form");
            form.target = "_blank";
            form.method = "POST";
            form.action = url;
            form.style.display = "none";
        
            for (var key in data) {
                var input = document.createElement("input");
                input.type = "hidden";
                input.name = key;
                input.value = data[key];
                form.appendChild(input);
            }
        
            document.body.appendChild(form);
            form.submit();
            document.body.removeChild(form);
        }
        
        function open_nnm_club(name) {
            var data = {
                nm : name
            };
            openWindowWithPost("https://nnm-club.me/forum/tracker.php", data);
        }
    </script>
    
    <table>
    <tr>
    <td style="vertical-align: top;">
    <table class="frame">
        <caption><a href="https://ru.wikipedia.org/wiki/Список_игр,_защищённых_Denuvo">Список взломанных игр</a></caption>
        <colgroup>
            <col span="1">
        </colgroup>
        <tbody>
            <tr>
            {% for header in cracked_headers %}
                <th>{{ header }}</th>
            {% endfor %}
            </tr>

        {% for name, _, _, crack_date, _ in cracked_games %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ name }}</td>
                <td>{{ crack_date }}</td>
                <td>
                    <button onclick="window.open(`https://rutracker.net/forum/tracker.php?nm={{ name }}`)">rutracker</button>
                    <button onclick="window.open(`http://anti-tor.org/search/0/8/000/0/{{ name }}`)">Rutor</button>
                    <button onclick="open_nnm_club(`{{ name }}`)">NNM-Club</button>
                    <button onclick="window.open(`https://fitgirl-repacks.site/?s={{ name }}`)">fitgirl</button>
                    <button onclick="window.open(`http://search.tfile.co/?q={{ name }}`)">tFile</button>
                    <button onclick="window.open(`http://www.torrentino.me/search?type=games&search={{ name }}`)">Torrentino</button>
                    <button onclick="window.open(`https://yandex.ru/yandsearch?text={{ name }}`)">Yandex</button>
                    <button onclick="window.open(`https://www.google.ru/#newwindow=1&q={{ name }}`)">Google</button>
                </td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    </td>
    
    <td width="10px"></td>
    
    <td style="vertical-align: top;">
    <table class="frame">
        <caption>Еще не взломали:<caption>
        <colgroup>
            <col span="1">
        </colgroup>
        <tbody>
            <tr>
            {% for header in not_cracked_headers %}
                <th>{{ header }}</th>
            {% endfor %}
            </tr>

        {% for name, release_date, days_passed in not_cracked_games %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ name }}</td>
                <td>{{ release_date }}</td>
                <td>{{ days_passed }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    
    </td>
    </tr>
    <table>
    
</body>
</html>
    """, cracked_headers=["№", "Название", "Дата взлома", "Поиск"], cracked_games=cracked_games,
         not_cracked_headers=["№", "Название", "Дата выхода", "Дней"], not_cracked_games=not_cracked_games
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
