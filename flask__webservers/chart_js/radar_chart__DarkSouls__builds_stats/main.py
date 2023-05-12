#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
from flask import Flask, render_template


app = Flask(__name__, static_folder="../static")
logging.basicConfig(level=logging.DEBUG)


title = "chart_js/radar_chart__DarkSouls__builds_stats"
labels = [
    "Vitality",
    "Attunement",
    "Endurance",
    "Strength",
    "Dexterity",
    "Resistance",
    "Intelligence",
    "Faith",
]
items = [
    {
        "name": "Cult Cleric Regen",
        "url": "https://darksouls.wiki.fextralife.com/Cult+Cleric+Regen",
        "color": "rgb(255, 99, 132)",
        "stats": [95, 12, 30, 16, 13, 10, 9, 16],
        "hidden": "true",
    },
    {
        "name": "Holy Dragon Knightess",
        "url": "https://darksouls.wiki.fextralife.com/Holy+Dragon+Knightess",
        "color": "rgb(255, 159, 64)",
        "stats": [26, 14, 36, 16, 10, 12, 8, 60],
        "hidden": "false",
    },
    {
        "name": "Royal Tank",
        "url": "https://darksouls.wiki.fextralife.com/Royal+Tank",
        "color": "rgb(75, 192, 192)",
        "stats": [50, 8, 40, 46, 10, 11, 8, 10],
        "hidden": "false",
    },
    {
        "name": "Vergil Style (Wanderer Style)",
        "url": "https://darksouls.wiki.fextralife.com/Vergil+Style",
        "color": "rgb(54, 162, 235)",
        "stats": [31, 12, 40, 16, 40, 12, 24, 8],
        "hidden": "false",
    },
    {
        "name": "Vergil Style (Thief Style)",
        "url": "https://darksouls.wiki.fextralife.com/Vergil+Style",
        "color": "rgb(153, 102, 255)",
        "stats": [28, 12, 40, 16, 40, 10, 24, 11],
        "hidden": "false",
    },
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        title=title,
        title_chart="DarkSouls builds stats",
        labels=labels,
        items=items,
    )


if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
