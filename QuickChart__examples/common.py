#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install quickchart.io
from quickchart import QuickChart


def get_chart() -> QuickChart:
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.version = "2"
    qc.background_color = ""
    qc.config = {
        "type": "doughnut",
        "data": {
            "datasets": [
                {
                    "data": [43, 21],
                    "backgroundColor": ["rgb(173 225 232)", "rgb(33 170 184)"],
                    "borderWidth": 0,
                },
            ],
        },
        "options": {
            "cutoutPercentage": 80,
            "legend": {
                "display": "false",
            },
            "plugins": {
                "datalabels": {
                    "display": "false",
                },
            },
        },
    }
    return qc
