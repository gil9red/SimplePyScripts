#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from flask import Flask, request
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


# Добавление пути основной папки репозитория, чтобы импортировать модуль download_volume_readmanga
import os
dir = os.path.dirname(__file__)
dir = os.path.dirname(dir)
dir = os.path.dirname(dir)

import sys
sys.path.append(dir)


# from itertools import chain

# from job_report import get_report_persons_info, get_person_info
from job_report import get_person_info


PEM_FILE_NAME = 'ipetrash.pem'


@app.route("/")
def index():
    # report_dict = get_report_persons_info(PEM_FILE_NAME)
    #
    # # Вывести всех сотрудников, отсортировав их по количестве переработанных часов
    # person_list = list(chain(*report_dict.values()))

    # # Проверка того, что сортировка работает (в принципе, думаю можно удалить)
    # assert sorted(person_list, key=lambda x: x.deviation_of_time) == \
    #        sorted(person_list, key=lambda x: x.deviation_of_time.total)
    #
    # sorted_person_list = sorted(person_list, key=lambda x: x.deviation_of_time, reverse=True)
    #
    # for i, person in enumerate(sorted_person_list, 1):
    #     print('{:>3}. {} {}'.format(i, person.full_name, person.deviation_of_time))
    #
    # print()
    #
    # found = list(filter(lambda x: x.second_name == 'Петраш', person_list))
    # if found:
    #     person = found[0]
    #     # return '#{}. {} {}'.format(sorted_person_list.index(person) + 1, person.full_name, person.deviation_of_time)
    #     return '{} {}'.format(person.full_name, person.deviation_of_time)

    # person = get_person_info(PEM_FILE_NAME, second_name='Петраш', first_name='Илья', report_dict=report_dict)
    person = get_person_info(PEM_FILE_NAME, second_name='Петраш')
    if person:
        return '{} {}'.format(person.full_name, person.deviation_of_time)

    return 'Not found specific user'


if __name__ == '__main__':
    # Localhost
    app.run(port=5001)

    # # Public IP
    # app.run(host='0.0.0.0')
