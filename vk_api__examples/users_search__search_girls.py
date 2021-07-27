#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as dt
import time
from collections import defaultdict

from root_common import get_vk_session


# Скрипт выполняет поиск в вк по заданным критериям и после фильтрует тех,
# у кого личка открыта и у которых дата последнего посещения меньше 7 дней


# https://github.com/python273/vk_api
# https://vk.com/dev/methods
# http://vk.com/dev/users.search
# http://vk.com/dev/fields
# http://vk.com/dev/fields_2


def get_title_relation(relation: int) -> str:
    # http://vk.com/dev/fields_2
    # relation:
    # 1 — не женат/не замужем
    # 2 — есть друг/есть подруга
    # 3 — помолвлен/помолвлена
    # 4 — женат/замужем
    # 5 — всё сложно
    # 6 — в активном поиске
    # 7 — влюблён/влюблена
    # 8 — в гражданском браке

    if relation == 0 or relation is None:
        return 'Не указано семейное положение'

    elif relation == 1:
        return 'Не женат/не замужем'

    elif relation == 2:
        return 'Есть друг/есть подруга'

    elif relation == 3:
        return 'Помолвлен/помолвлена'

    elif relation == 4:
        return 'Женат/замужем'

    elif relation == 5:
        return 'Всё сложно'

    elif relation == 6:
        return 'В активном поиске'

    elif relation == 7:
        return 'Влюблён/влюблена'

    elif relation == 8:
        return 'В гражданском браке'

    else:
        return f'Error! Unknown relation = {relation}!'


if __name__ == '__main__':
    vk_session = get_vk_session()

    server_time = vk_session.method('utils.getServerTime')
    server_time = dt.datetime.fromtimestamp(server_time)

    params = {
        'sex': 1,  # Женский пол
        'age_from': 18,  # Возраст от
        'age_to': 25,  # Возраст до
        'hometown': 'Магнитогорск',  # Город
        'city': 82,  # id города
        'status': 0,  # 0 - любое семейное положение

        # Дополнительные поля, которые вернутся в ответе
        'fields': ','.join([
            'last_seen',  # Время последнего посещения
            'can_write_private_message',  # Разрешено ли написание личных сообщений данному пользователю
            'relation',  # Семейное положение
        ]),

        'offset': 1,  # Смещение относительно первого найденного пользователя
        'count': 1000,  # Количество возвращаемых пользователей (1000 это максимум)
    }

    rs = vk_session.method('users.search', params)

    # Список id пользователей
    user_list_id = []

    # При первом запросе, настроен поиск пользователей с любым семейным положением,
    # поэтому отфильтруем его и оставим только пользователей с нужным нам семейным положением
    for user in rs['items']:
        # Семейное положение
        relation = user.get('relation')

        # Нужное семейное положение: 1, 5, 6 или оно пусть не указано пользователем (relation = None или 0)
        needed_relation = relation == 1 or relation == 5 or relation == 6 or relation is None or relation == 0
        if needed_relation:
            user_list_id.append(user)

    # На всякий случай подождем немного (вк не разрешает обращаться чаще 3 раза в секунду)
    time.sleep(0.4)

    # Теперь ищем тех, у кого статус "не женат/не замужем"
    params['status'] = 1
    rs = vk_session.method('users.search', params)
    user_list_id.extend(rs.get('items'))

    # На всякий случай подождем немного (вк не разрешает обращаться чаще 3 раза в секунду)
    time.sleep(0.4)

    # Теперь ищем тех, у кого статус "всё сложно"
    params['status'] = 5
    rs = vk_session.method('users.search', params)
    user_list_id.extend(rs.get('items'))

    # На всякий случай подождем немного (вк не разрешает обращаться чаще 3 раза в секунду)
    time.sleep(0.4)

    # Теперь ищем тех, у кого статус "в активном поиске"
    params['status'] = 6
    rs = vk_session.method('users.search', params)
    user_list_id.extend(rs.get('items'))

    # Отфильтрованный список id юзеров
    filtered_users_id = []

    # Группирование по семейному положению:
    # ключом является семейное положение, а его значением список id пользователей
    relation_group_users = defaultdict(list)

    for user in user_list_id:
        user_id = user['id']

        # Из-за алгоритма поиска возможны дупликаты id пользователей,
        # которых нет смысла обрабатывать снова
        if user_id in filtered_users_id:
            continue

        # Личка закрыта или неизвестна дата последнего посещения
        if not user['can_write_private_message'] or 'last_seen' not in user:
            continue

        # Дата последнего посещения
        last_seen = user['last_seen']['time']
        last_seen = dt.datetime.fromtimestamp(last_seen)

        # Нет онлайн 7 или больше дней
        if server_time - last_seen >= dt.timedelta(days=7):
            continue

        # Добавим пользователя, прошедшего фильтр, в список
        filtered_users_id.append(user_id)

        # По сути, если relation = 0, или если relation не было возвращено
        # означает одно и тоже - семейное положение не указано
        relation = user.get('relation', 0)

        relation_group_users[relation].append(user_id)

    print(f'Всего найдено: {len(filtered_users_id)}\n')

    for relation, users in relation_group_users.items():
        print(f'{get_title_relation(relation)} ({len(users)}):')

        for i, user_id in enumerate(users, 1):
            print(f'{i}. https://vk.com/id{user_id}')

        print()
