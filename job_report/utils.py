#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from datetime import datetime
from collections import defaultdict
import os.path
from itertools import chain

import requests
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup

from job_report.report_person import ReportPerson


URL = 'https://jira.compassplus.ru/pa-reports/'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'

LOGGING_DEBUG = False


if LOGGING_DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)


def get_report_context(pem_file_name):
    headers = {
        'User-Agent': USER_AGENT
    }

    rs = requests.get(URL, headers=headers, cert=pem_file_name, verify=False)
    if LOGGING_DEBUG:
        print('rs=', rs)
        print('rs.request.headers=', rs.request.headers)
        print('rs.headers=', rs.headers)

    today = datetime.today()
    data = {
        'dep': 'all',
        'rep': 'rep3',
        'period': today.strftime('%Y-%m'),
        'v': int(today.timestamp() * 1000),
        'type': 'normal',
    }

    headers = {
        'cookie': rs.headers['set-cookie'],
        'User-Agent': USER_AGENT,
    }

    rs = requests.post(URL, data=data, headers=headers, cert=pem_file_name, verify=False)
    if LOGGING_DEBUG:
        print('rs=', rs)
        print('rs.request.headers=', rs.request.headers)
        print('rs.headers=', rs.headers)

    return rs.text


def get_report_persons_info(pem_file_name):
    today = datetime.today().strftime('%d%m%y')
    report_file_name = 'report_{}.html'.format(today)

    # Если кэш-файл отчета не существует, загружаем новые данные и сохраняем в кэш-файл
    if not os.path.exists(report_file_name):
        if LOGGING_DEBUG:
            print('{} not exist'.format(report_file_name))

        context = get_report_context(pem_file_name)

        with open(report_file_name, mode='w', encoding='utf-8') as f:
            f.write(context)
    else:
        if LOGGING_DEBUG:
            print('{} exist'.format(report_file_name))

        with open(report_file_name, encoding='utf-8') as f:
            context = f.read()

    html = BeautifulSoup(context, 'lxml')
    report = html.select('#report tbody tr')

    current_dep = None

    report_dict = defaultdict(set)

    for row in report:
        children = list(row.children)
        if len(children) == 1 and children[0].name == 'th':
            current_dep = children[0].text.strip()
            continue

        if children[0].has_attr('class') and children[0].attrs['class'][0] == 'person':
            person_tags = [children[0].text] + [i.text for i in row.nextSibling.select('td')[1:]]
            person = ReportPerson(person_tags)

            report_dict[current_dep].add(person)

    return report_dict


def get_person_info(pem_file_name, second_name, first_name=None, middle_name=None, report_dict=None):
    if report_dict is None:
        report_dict = get_report_persons_info(pem_file_name)

    # Вывести всех сотрудников, отсортировав их по количеству переработанных часов
    for person in list(chain(*report_dict.values())):
        found = person.second_name == second_name

        if first_name is not None:
            found = found and person.first_name == first_name

        if middle_name is not None:
            found = found and person.middle_name == middle_name

        if found:
            return person
