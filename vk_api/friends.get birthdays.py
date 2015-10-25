# -*- coding: utf-8 -*-

from operator import itemgetter
import sys
import datetime

import vk_api


__author__ = 'ipetrash'

"""Скрипт выводит список друзей пользователя и показывает сколько дней
осталось до их дней рождения.
Список упорядочен по количеству оставшихся до дня рождения дней."""


def vk_bdate_to_bdate_this_year(bdate):
    # bdate может быть в формате: %d.%m.%Y или %d.%m
    parts = bdate.split('.')
    d, m, y = int(parts[0]), int(parts[1]), datetime.datetime.today().year
    return datetime.date(y, m, d)


# https://github.com/python273/vk_api
# https://vk.com/dev/methods


def vk_auth(login, password):
    vk = vk_api.VkApi(login, password)

    try:
        vk.authorization()  # Авторизируемся
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)  # В случае ошибки выведем сообщение
        sys.exit()

    return vk


LOGIN = ''
PASSWORD = ''

if __name__ == '__main__':
    # Авторизируемся
    vk = vk_auth(LOGIN, PASSWORD)

    # Получим и выведем список друзей с указанными днями рождения
    # Если не указывать user_id, то вернется список друзей текущего пользователя,
    # того чьи логин и пароль использовались для авторизации, соответственно, если указать
    # user_id, то выведется список конкретного пользователя.
    rs = vk.method('friends.get', {
        # 'user_id': '4033640',
        'fields': 'bdate',
    })

    # Список друзей у которых день рождения еще не наступил в этом году
    filtered_friends = []

    for friend in rs.get('items'):
        bdate = friend.get('bdate')
        if bdate:
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
    sorted_by_bdate_list = sorted(filtered_friends, key=itemgetter('remained_days'))
    if not sorted_by_bdate_list:
        print('В этом году у всех друзей уже были дни рождения.')
        quit()

    # Выведем отсортированный список друзей
    for i, friend in enumerate(sorted_by_bdate_list, 1):
        id_user = friend.get('id')
        first_name = friend.get('first_name')
        last_name = friend.get('last_name')
        remained_days = friend.get('remained_days')

        print("{}. {} (id{}) до дня рождения осталось {} дней".format(
            i,
            first_name + " " + last_name,
            id_user,
            remained_days,
        ))
