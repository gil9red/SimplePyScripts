#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт перебираем все комментарии и подсчитывает количество комментариев людей. Получится словарь
у которого ключом будет id пользователя, а значением - количество его комментариев.
"""


from collections import defaultdict
from vk_api import VkTools
from root_common import get_vk_session


# EXAMPLE: https://vk.com/okami_avtorolls?w=wall-43006068_49200
OWNER_ID = -43006068
POST_ID = 49200


if __name__ == '__main__':
    vk_session = get_vk_session()
    tools = VkTools(vk_session)

    user_comment_count_dict = defaultdict(int)

    data = {
        'owner_id': OWNER_ID,
        'post_id': POST_ID,
    }
    wall_it = tools.get_all_iter('wall.getComments', 100, data)
    for item in wall_it:
        user_id = item.get('from_id')
        if user_id:
            user_comment_count_dict[user_id] += 1

    print(f'Закончено получение данных. Всего пользователей комментировало: {len(user_comment_count_dict)}.')
    print('Вывожу пользователей и количество их комментариев:')

    # TODO: по id вывести имя/фамилию/пол/url-страницы
    # Выведем в порядке убывания по количеству комментариев от пользователя
    for k, v in sorted(user_comment_count_dict.items(), key=lambda x: x[1], reverse=True):
        print(f'  {k}: {v}')
