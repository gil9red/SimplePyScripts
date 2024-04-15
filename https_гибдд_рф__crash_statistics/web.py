#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt

from flask import Flask, render_template
from common import get_crash_statistics_list_db


app = Flask(__name__)


@app.route("/")
def index():
    headers = ["Дата", "ДТП", "Погибли", "Погибло детей", "Ранены", "Ранено детей"]
    rows = get_crash_statistics_list_db()
    rows.reverse()

    data: list[dict] = []
    year_by_number: dict[int, int] = dict()
    for date_str, dtp, died, children_died, wounded, wounded_children in rows:
        date = dt.datetime.strptime(date_str, "%d.%m.%Y").date()
        dtp = int(dtp)

        data.append({
            "date": date_str,
            "date_iso": date.isoformat(),
            "dtp": dtp,
            "died": int(died),
            "children_died": int(children_died),
            "wounded": int(wounded),
            "wounded_children": int(wounded_children),
        })

        if date.year not in year_by_number:
            year_by_number[date.year] = 0
        year_by_number[date.year] += dtp

    return render_template(
        "index.html",
        title="АВАРИЙНОСТЬ НА ДОРОГАХ РОССИИ",
        headers=headers,
        data=data,
        year_by_number=year_by_number,
    )


if __name__ == "__main__":
    app.debug = True

    # Localhost
    app.run(port=10009)

    # # Public IP
    # app.run(host='0.0.0.0')
