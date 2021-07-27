#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт выводит список друзей пользователя и показывает сколько дней осталось до их дней рождения.
Список упорядочен по количеству оставшихся до дня рождения дней.
"""

# https://github.com/python273/vk_api
# https://vk.com/dev/methods


import datetime
import sys

from root_common import get_vk_session


def vk_bdate_to_bdate_this_year(bdate):
    # bdate может быть в формате: %d.%m.%Y или %d.%m
    parts = bdate.split('.')
    d, m, y = int(parts[0]), int(parts[1]), datetime.datetime.today().year
    return datetime.date(y, m, d)


if __name__ == '__main__':
    # Авторизируемся
    vk_session = get_vk_session()
    vk = vk_session.get_api()

    # Получим и выведем список друзей с указанными днями рождения
    # Если не указывать user_id, то вернется список друзей текущего пользователя,
    # того чьи логин и пароль использовались для авторизации, соответственно, если указать
    # user_id, то выведется список конкретного пользователя.
    rs = vk.friends.get(fields='bdate')
    # rs = vk.friends.get(fields='bdate', user_id=4033640)

    # Список друзей у которых день рождения еще не наступил в этом году
    filtered_friends = []

    for friend in rs.get('items'):
        bdate = friend.get('bdate')
        if not bdate:
            continue

        # Дата дня рождения в текущем году
        birthday_this_year = vk_bdate_to_bdate_this_year(bdate)

        # Сколько осталось дней до дня рождения
        remained_days = birthday_this_year - datetime.datetime.today().date()
        remained_days = remained_days.days

        if remained_days > 0:
            # Добавим в словарь пользователя сколько дней осталось до его дня рождения
            friend['remained_days'] = remained_days
            filtered_friends.append(friend)

    # Отсортируем список друзей по тому сколько осталось дней до их дня рождения
    sorted_by_bdate_list = sorted(filtered_friends, key=lambda x: x['remained_days'])
    if not sorted_by_bdate_list:
        print('В этом году у всех друзей уже были дни рождения.')
        sys.exit()

    # Выведем отсортированный список друзей
    for i, friend in enumerate(sorted_by_bdate_list, 1):
        id_user = friend.get('id')
        first_name = friend.get('first_name')
        last_name = friend.get('last_name')
        remained_days = friend.get('remained_days')

        print(f"{i}. {first_name} {last_name} (id{id_user}) до дня рождения осталось {remained_days} дней")
