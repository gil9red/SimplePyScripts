#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/twbs/bootstrap
# SOURCE: https://github.com/twbs/bootstrap/releases
# SOURCE: https://getbootstrap.com/docs/4.3/components/badge/


import logging
from typing import NamedTuple

from flask import Flask, render_template


app = Flask(__name__, static_folder="../_static")

logging.basicConfig(level=logging.DEBUG)


class Genre(NamedTuple):
    name: str
    description: str = ""


GENRE__SURVIVAL_HORROR = Genre("survival horror")
GENRE__TPS = Genre(name="TPS", description="Third-person shooter")
GENRE__RPG = Genre(name="RPG", description="Role playing game")
GENRE__ACTION = Genre("Action")
GENRE__ACTION_ADVENTURE = Genre("Action-adventure")


@app.route("/")
def index():
    items = [
        {
            "name": "Dead Space",
            "url": "https://ru.wikipedia.org/wiki/Dead_Space",
            "genres": [
                GENRE__SURVIVAL_HORROR,
                GENRE__TPS,
            ],
        },
        {
            "name": "Dead Island",
            "url": "https://ru.wikipedia.org/wiki/Dead_Island",
            "genres": [
                GENRE__SURVIVAL_HORROR,
                GENRE__RPG,
            ],
        },
        {
            "name": "Dying Light",
            "url": "https://ru.wikipedia.org/wiki/Dying_Light",
            "genres": [
                GENRE__SURVIVAL_HORROR,
                GENRE__ACTION,
                GENRE__RPG,
            ],
        },
        {
            "name": "Dark Souls",
            "url": "https://ru.wikipedia.org/wiki/Dark_Souls",
            "genres": [
                GENRE__ACTION,
                GENRE__RPG,
            ],
        },
        {
            "name": "Darksiders III",
            "url": "https://ru.wikipedia.org/wiki/Darksiders_III",
            "genres": [
                GENRE__ACTION,
                GENRE__RPG,
                GENRE__ACTION_ADVENTURE,
            ],
        },
    ]
    columns = ["NAME", "URL", "GENRES"]

    return render_template("index.html", columns=columns, items=items)


if __name__ == "__main__":
    app.debug = True

    # Localhost
    # port=0 -- random free port
    # app.run(port=0)
    app.run(port=5000)

    # # Public IP
    # app.run(host='0.0.0.0')
