#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# p12 to pem:
#     C:\Users\ipetrash>openssl pkcs12 -in ipetrash.p12 -out ipetrash.pem -nodes -clcerts
#     Enter Import Password:
#     MAC verified OK
# OR:
#     OpenSSL_example\p12_to_pem.py

PEM_FILE_NAME = 'ipetrash.pem'


if __name__ == '__main__':
    from job_report.utils import get_report_persons_info
    report_dict = get_report_persons_info(PEM_FILE_NAME)

    # Вывести всех сотрудников, отсортировав их по количестве переработанных часов
    from itertools import chain
    person_list = list(chain(*report_dict.values()))

    # Проверка того, что сортировка работает (в принципе, думаю можно удалить)
    assert sorted(person_list, key=lambda x: x.deviation_of_time) == \
           sorted(person_list, key=lambda x: x.deviation_of_time.total)

    sorted_person_list = sorted(person_list, key=lambda x: x.deviation_of_time, reverse=True)

    for i, person in enumerate(sorted_person_list, 1):
        print('{:>3}. {} {}'.format(i, person.full_name, person.deviation_of_time))

    print()
    found = list(filter(lambda x: x.second_name == 'Петраш', person_list))
    if found:
        person = found[0]
        print('#{}. {} {}'.format(sorted_person_list.index(person) + 1, person.full_name, person.deviation_of_time))
