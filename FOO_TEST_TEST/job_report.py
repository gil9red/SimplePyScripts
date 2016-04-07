#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
requests.packages.urllib3.disable_warnings()


from datetime import datetime
from bs4 import BeautifulSoup
from collections import defaultdict
from functools import total_ordering


class ReportPerson:
    """Класс для описания сотрудника в отчете."""

    def __init__(self, tags):
        # ФИО
        self.second_name, self.first_name, self.middle_name = tags[0].split()

        # Невыходов на работу
        self.absence_from_work = int(tags[1])

        # По календарю (смен / ч:мин)
        # Для точного значения посещенных дней, может быть указано как "3 = 4- (1 О)", поэтому
        # отсекаем правую, от знака равно, сторону, удаляем пробелы и переводим в число
        self.need_to_work_days = self.get_work_day(tags[2])
        self.need_to_work_on_time = self.get_work_time(tags[3])

        # Фактически (смен / ч:мин)
        self.worked_days = self.get_work_day(tags[4])
        self.worked_time = self.get_work_time(tags[5])

        # Отклонение (смен / ч:мин)
        self.deviation_of_day = self.get_work_day(tags[6])
        self.deviation_of_time = self.get_work_time(tags[7])

    @property
    def full_name(self):
        return self.second_name + ' ' + self.first_name + ' ' + self.middle_name

    @staticmethod
    def get_work_day(day_str):
        return int(day_str) if '=' not in day_str else int(day_str.split('=')[0].strip())

    @total_ordering
    class Time:
        """Простой класс для хранения даты работы."""

        def __init__(self, time_str):
            self._hours, self._minutes = map(int, time_str.split(':'))

        @property
        def total(self):
            """Всего минут"""

            return self._hours * 60 + self._minutes

        def __repr__(self):
            return "{:0>2}:{:0>2}".format(self._hours, self._minutes)

        def __eq__(self, other):
            return self.total == other.total

        def __lt__(self, other):
            return self.total < other.total

    @staticmethod
    def get_work_time(time_str):
        return ReportPerson.Time(time_str)

    def __repr__(self):
        return "{}. Невыходов на работу: {}. По календарю ({} смен / {} ч:мин). " \
               "Фактически ({} смен / {} ч:мин) Отклонение ({} смен / {} ч:мин)".format(self.full_name,
                                                                                        self.absence_from_work,
                                                                                        self.need_to_work_days,
                                                                                        self.need_to_work_on_time,
                                                                                        self.worked_days,
                                                                                        self.worked_time,
                                                                                        self.deviation_of_day,
                                                                                        self.deviation_of_time,
                                                                                        )

# TODO: webserver


# p12 to pem:
#     C:\Users\ipetrash>openssl pkcs12 -in ipetrash.p12 -out ipetrash.pem -nodes -clcerts
#     Enter Import Password:
#     MAC verified OK
# OR:
#     OpenSSL_example\p12_to_pem.py


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'
URL = 'https://confluence.compassplus.ru/reports/index.jsp'
PEM_FILE_NAME = 'ipetrash.pem'
LOGGING_DEBUG = False


if LOGGING_DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)


def get_report_context():
    headers = {
        'User-Agent': USER_AGENT
    }

    rs = requests.get(URL, headers=headers, cert=PEM_FILE_NAME, verify=False)
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

    rs = requests.post(URL, data=data, headers=headers, cert=PEM_FILE_NAME, verify=False)
    if LOGGING_DEBUG:
        print('rs=', rs)
        print('rs.request.headers=', rs.request.headers)
        print('rs.headers=', rs.headers)

    return rs.text


def get_report_persons_info():
    context = get_report_context()

    html = BeautifulSoup(context, 'lxml')
    report = html.select('#report tbody tr')

    current_dep = None

    report_dict = defaultdict(list)

    for row in report:
        children = list(row.children)
        if len(children) == 1 and children[0].name == 'th':
            current_dep = children[0].text
            continue

        if children[0].has_attr('class') and children[0].attrs['class'][0] == 'person':
            person_tags = [children[0].text] + [i.text for i in row.nextSibling.select('td')[1:]]
            person = ReportPerson(person_tags)

            report_dict[current_dep].append(person)

    return report_dict


if __name__ == '__main__':
    report_dict = get_report_persons_info()

    # Вывести всех сотрудников, отсортировав их по количестве переработанных часов
    from itertools import chain
    person_list = list(chain(*report_dict.values()))

    # Проверка того, что сортировка работает (в принципе, думаю можно удалить)
    assert sorted(person_list, key=lambda x: x.deviation_of_time) == \
           sorted(person_list, key=lambda x: x.deviation_of_time.total)

    for i, person in enumerate(sorted(person_list, key=lambda x: x.deviation_of_time, reverse=True), 1):
        print('{}. {}'.format(i, person.full_name), person.deviation_of_time)

    print()
    found = list(filter(lambda x: x.second_name == 'Петраш', person_list))
    if found:
        print(found[0].full_name, found[0].deviation_of_time)
