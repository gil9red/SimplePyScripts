#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Скрипт перебираем все комментарии и подсчитывает количество комментариев людей. Получится словарь
у которого ключом будет id пользователя, а значением -- количество его комментариев."""


# https://vk.com/wall-37473310_377390


from collections import defaultdict

import time
import traceback
import sys

import vk_api


LOGIN, PASSWORD = '', ''
OWNER_ID = ''
POST_ID = ''
USER_ID = ''


if __name__ == '__main__':
    vk = vk_api.VkApi(LOGIN, PASSWORD)

    try:
        vk.auth()
    except Exception as e:
        print(e)
        sys.exit()

    user_comment_count_dict = defaultdict(int)

    offset = 0
    count = 100
    count_comments = None

    while True:
        try:
            count_comments_title = 'unknown' if count_comments is None else count_comments
            print(f'Запрашиваю порцию данных: offset={offset}, count={count}, count_comments={count_comments_title}.')

            data = {
                'owner_id': OWNER_ID,
                'post_id': POST_ID,
                'count': count,
                'offset': offset,
            }
            rs = vk.method('wall.getComments', data)
            count_comments = int(rs['count'])

            # Ищем комментарий, оставленный user_id
            for item in rs['items']:
                user_id = item['from_id']
                user_comment_count_dict[user_id] += 1

            if offset >= count_comments:
                break

            offset += count
            time.sleep(0.4)

        except Exception as e:
            print(f'Ошибка:\n{traceback.format_exc()}')
            print('Ждем 60 секунд.')
            time.sleep(60)

    print(f'Закончено получение данных. Всего пользователей комментировало: {len(user_comment_count_dict)}.')
    print('Вывожу пользователей и количество их комментариев:')

    # TODO: по id вывести имя/фамилию/пол/url-страницы
    # Выведем в порядке убывания по количеству комментариев от пользователя
    for k, v in sorted(user_comment_count_dict.items(), key=lambda x: x[1], reverse=True):
        print('  {}: {}'.format(k, v))
