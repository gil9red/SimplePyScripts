#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, render_template_string
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    from common import FINISHED, FINISHED_WATCHED, create_connect
    connect = create_connect()
    try:
        cursor = connect.cursor()

        get_game_sql = '''
            SELECT name, price
            FROM game
            WHERE kind = ?
            ORDER BY name
        '''
        finished_games = cursor.execute(get_game_sql, (FINISHED,)).fetchall()
        finished_watched_games = cursor.execute(get_game_sql, (FINISHED_WATCHED,)).fetchall()

        # NOTE: вычисление такого можно было перенести на клиента и описать через javascript
        # но т.к. данных мало и пользоваться ими будут очень редко, можно на серверной стороне
        # их считать.
        # Это будет касаться и подсчета сумм.

        def statistic_string(games):
            """
            Функция возвращает строку с статистикой: сколько всего игр, сколько имеют цены, и процент.
            Пример: (0 / 160 (0%))

            """

            price_number = len([item for item in games if item[1] is not None])
            return '({} / {} ({:.0f}%))'.format(
                price_number,
                len(games),
                price_number / len(games) * 100
            )

        finished_game_statistic = statistic_string(finished_games)
        finished_watched_game_statistic = statistic_string(finished_watched_games)

    finally:
        connect.close()

    headers = ['NAME', 'PRICE']

    return render_template_string('''\
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Список игр</title>

    <style type="text/css">
        /* Увеличим заголовок таблиц */
        table > caption {
            font-size: 150%;
        }

        /* Небольшой отступ внутри ячеек */
        td, th {
            padding: 5px;
        }

        .price_is_none {
            background-color: lightgray;
        }
    </style>
</head>
<body>
    <table id="finished_game" width="70%" border="1">
        <caption>Пройденные игры {{ finished_game_statistic }}</caption>
        <tr>
        {% for header in headers %}
            <th>{{ header }}</th>
        {% endfor %}
        </tr>

        {% for name, price in finished_games %}
            <tr><td>{{ name }}</td><td>{{ price }}</td></tr>
        {% endfor %}
    </table>
    <br><br><br>

    <table id="finished_watched_game" width="70%" border="1">
        <caption>Просмотренные игры {{ finished_watched_game_statistic }}</caption>
        <tr>
        {% for header in headers %}
            <th>{{ header }}</th>
        {% endfor %}
        </tr>

        {% for name, price in finished_watched_games %}
            <tr><td>{{ name }}</td><td>{{ price }}</td></tr>
        {% endfor %}
    </table>

    <script>
        // Функция выделяет те игры, в которых еще не указана цена
        function fill_background_game_with_empty_price(table_id) {
            var rows = document.getElementById(table_id).rows;

            // Пропускаем первую строку, т.к. это заголовок
            for (var i = 1; i < rows.length; i++) {
                var name = rows[i].cells[0];
                var price = rows[i].cells[1];

                if (price.innerHTML == "None") {
                    name.className += " price_is_none";
                    price.className += " price_is_none";
                }
            }
        }

        fill_background_game_with_empty_price("finished_game");
        fill_background_game_with_empty_price("finished_watched_game");
    </script>
</body>
</html>
''',
        headers=headers,
        finished_games=finished_games, finished_watched_games=finished_watched_games,
        finished_game_statistic=finished_game_statistic,
        finished_watched_game_statistic=finished_watched_game_statistic
    )


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

