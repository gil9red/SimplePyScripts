#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# NOTE: вычисление такого можно было перенести на клиента и описать через javascript
# но т.к. данных мало и пользоваться ими будут очень редко, можно на серверной стороне
# их считать.
# Это будет касаться и подсчета сумм.
def statistic_string(games):
    """
    Функция возвращает строку с статистикой: сколько всего игр, сколько имеют цены, и процент.
    Пример: (0 / 160 (0%))

    """

    price_number = len([(name, price) for name, price in games if price is not None])
    return '({} / {} ({:.0f}%))'.format(
        price_number,
        len(games),
        price_number / len(games) * 100
    )


def total_price(games):
    """
    Функция подсчитает и вернет сумму цен игр в списке.

    """

    def get_price(price_title):
        """Функция удаляет из получаемое строки все символы кроме цифровых и точки."""

        # TODO: быстрый вариант решения проблемы, но не надежный
        price = price_title.replace(' pуб.', '').strip()
        return float(price)

    total = sum(get_price(price) for _, price in games if price is not None)

    # Чтобы избавиться от пустой дробной части: 50087.0 -> 50087
    return total if total != int(total) else int(total)


from flask import Flask, render_template_string
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    from common import FINISHED, FINISHED_WATCHED, create_connect, settings
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

    finally:
        connect.close()

    finished_game_statistic = statistic_string(finished_games)
    finished_watched_game_statistic = statistic_string(finished_watched_games)

    total_price_finished_games = total_price(finished_games)
    total_price_finished_watched_games = total_price(finished_watched_games)

    headers = ['Название', 'Цена']

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

        th {
            font-size: 120%;
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
    Последнее обновление было: {{ last_run_date }}
    <br>

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

        <tr><td align="right">Итого:</td><td>{{ total_price_finished_games }}</td></tr>
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

        <tr><td align="right">Итого:</td><td>{{ total_price_finished_watched_games }}</td></tr>
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
        finished_watched_game_statistic=finished_watched_game_statistic,
        total_price_finished_games=total_price_finished_games,
        total_price_finished_watched_games=total_price_finished_watched_games,
        last_run_date=settings.last_run_date,
    )


if __name__ == '__main__':
    # Localhost
    app.debug = True

    app.run(
        port=5000,

        # NOTE: убрал т.к. вызывало при получении запроса ошибку "sqlite3.ProgrammingError: SQLite objects created
        # in a thread can only be used in that same thread.The object was created in thread id 9284 and this is"
        # а разбираться с этим не было желания
        #
        # # Включение поддержки множества подключений
        # threaded=True,
    )

    # # Public IP
    # app.run(host='0.0.0.0')
