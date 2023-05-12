#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Чтение из docx файла таблицы меню и отображении таблицы на веб странице.

Устанавливать docx так: pip install python-docx
"""


import logging
import re

from docx import Document
from flask import Flask, render_template_string


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Регулярка для поиска последовательностей пробелов: от двух подряд и более
multi_space_pattern = re.compile(r"[ ]{2,}")


def get_rows_lunch_menu():
    document = Document("lunch_menu.docx")

    rows = list()

    for table in document.tables:
        # Перебор начинается со второй строки, потому что, первая строка таблицы -- это строка "Обеденное меню"
        for row in table.rows[1:]:
            name, weight, price = [
                multi_space_pattern.sub(" ", i.text.strip())
                for i in row.cells
            ]

            if name == weight == price or (not weight or not price):
                name = name.title()
                logging.debug(name)
                rows.append((name,))
                continue

            rows.append((name, weight, price))
            logging.debug(f"{name} {weight} {price}")

        # Таблицы в меню дублируются
        break

    return rows


@app.route("/")
def index():
    rows = get_rows_lunch_menu()

    return render_template_string(
        """\
    <html>
    <head>
        <title>Обеденное меню</title>
        <link rel="stylesheet" href="static/style.css">
    </head>

    <body>

    <table>
        <tr><th colspan="3" align="center">Обеденное меню</th></tr>
        <tr><th>Название</th><th>Вес</th><th>Цена</th></tr>
        {% for row in rows %}

            {% if row|length == 3 %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                </tr>
            {% else %}
                <tr>
                    <td class="category" colspan="3">{{ row[0] }}</td>
                </tr>
            {% endif %}
        {% endfor %}
    </table>

    </body>
    </html>
    """,
        rows=rows,
    )


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
