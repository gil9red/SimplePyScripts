#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Вывод переработки текущего (или конкретного) пользователя"""


import logging
import sys
from pathlib import Path

from flask import Flask

DIR = Path(__file__).resolve().parent
sys.path.append(str(DIR.parent / "job_report"))
from utils import get_report_persons_info, get_person_info


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    report_dict = get_report_persons_info()

    try:
        person = report_dict["Текущий пользователь"][0]
    except:
        person = None

    if person is None:
        person = get_person_info(second_name="Петраш", report_dict=report_dict)

    if person:
        return f"{person.full_name} {person.deviation_of_time}"

    return "Not found specific user"


if __name__ == "__main__":
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
