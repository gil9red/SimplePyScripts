#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


class ReportPerson:
    """Класс для описания сотрудника в отчете."""

    def __init__(self, tags):
        # ФИО
        self.second_name, self.first_name, self.middle_name = tags[0].split()

        # Невыходов на работу
        self.absence_from_work = int(tags[1])

        # По календарю (смен / ч:мин)
        # self.need_to_work_days = tags[2]
        # Для точного значения посещенных дней, может быть указано как "3 = 4- (1 О)", поэтому
        # отсекаем правую, от знака равно, сторону, удаляем пробелы и переводим в число
        self.need_to_work_days = int(tags[2]) if '=' not in tags[2] else int(tags[2].split('=')[0].strip())
        self.need_to_work_on_time = tags[3]

        # Фактически (смен / ч:мин)
        self.worked_days = int(tags[4])
        self.worked_time = tags[5]

        # Отклонение (смен / ч:мин)
        self.deviation_of_day = int(tags[6])
        self.deviation_of_time = tags[7]

    def __repr__(self):
        return "{} {} {}. Невыходов на работу: {}. По календарю ({} смен / {} ч:мин). " \
               "Фактически ({} смен / {} ч:мин) Отклонение ({} смен / {} ч:мин)".format(self.second_name,
                                                                                        self.first_name,
                                                                                        self.middle_name,
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
LOGGING_DEBUG = False
PEM_FILE_NAME = 'ipetrash.pem'


if LOGGING_DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)


import requests
requests.packages.urllib3.disable_warnings()


from datetime import datetime


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

    from bs4 import BeautifulSoup
    html = BeautifulSoup(context, 'lxml')
    report = html.select('#report tbody tr')

    current_dep = None

    from collections import defaultdict
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

    for k, v in sorted(report_dict.items(), key=lambda x: len(x[0])):
        # found = list(filter(lambda x: x.second_name == 'Петраш', v))
        # if found:
        #     print(found[0])

        print('{} ({}):'.format(k, len(v)))
        for i, person in enumerate(v, 1):
            print('    {}. {}'.format(i, person))

        print()
