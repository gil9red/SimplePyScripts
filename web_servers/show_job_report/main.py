#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Вывод переработки текущего (или конкретного) пользователя"""


from flask import Flask
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


# Добавление пути основной папки репозитория, чтобы импортировать из job_report.utils
import os
dir = os.path.dirname(__file__)
dir = os.path.dirname(dir)
dir = os.path.dirname(dir)

import sys
sys.path.append(dir)


from job_report.utils import get_report_persons_info, get_person_info


PEM_FILE_NAME = 'ipetrash.pem'


@app.route("/")
def index():
    report_dict = get_report_persons_info(PEM_FILE_NAME)

    try:
        person = report_dict['Текущий пользователь'][0]
    except:
        person = None

    if person is None:
        person = get_person_info(PEM_FILE_NAME, second_name='Петраш', report_dict=report_dict)

    if person:
        return '{} {}'.format(person.full_name, person.deviation_of_time)

    return 'Not found specific user'


if __name__ == '__main__':
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
