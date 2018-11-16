# -*- coding: utf-8 -*-

import sys
# import time
# import datetime

import vk_api


__author__ = 'ipetrash'


# https://github.com/python273/vk_api
# https://vk.com/dev/methods


def vk_auth(login, password):
    vk = vk_api.VkApi(login, password)

    try:
        vk.auth()  # Авторизируемся
    except vk_api.AuthError as e:
        print(e)  # В случае ошибки выведем сообщение
        sys.exit()

    return vk


LOGIN = ''
PASSWORD = ''


if __name__ == '__main__':
    # Авторизируемся
    vk = vk_auth(LOGIN, PASSWORD)


    ## Лайкаем все посты указанного пользователяЫ
    # from time import sleep
    #
    # offset = 0
    # step = 100
    # max_post = 0
    # like_count = 0
    # sleep_timeout = 0.8
    #
    # while True:
    #     try:
    #         rs = vk.method(
    #             'wall.get', {
    #                 'owner_id': 666,
    #                 'offset': offset,
    #                 'count': step,
    #                 'filter': 'owner'
    #             }
    #         )
    #
    #         max_post = rs['count']
    #
    #         for post in rs['items']:
    #             post_id = post['id']
    #             post_owner_id = post['owner_id']
    #
    #             sleep(sleep_timeout)
    #
    #             rs = vk.method(
    #                 'likes.add', {
    #                     'type': 'post',
    #                     'owner_id': post_owner_id,
    #                     'item_id': post_id
    #                 }
    #             )
    #
    #             like_count += 1
    #             print('max_post: {}, like_count: {}, post_id: {}'.format(max_post, like_count, post_id))
    #
    #         offset += step
    #         if offset >= max_post:
    #             break
    #
    #     except vk_api.Captcha as e:
    #         print('Error: "{}", sleep_timeout: {}'.format(e, sleep_timeout))
    #         sleep_timeout += 0.2
    #         sleep(60)



    # http://vk.com/dev/storage.get
    # http://vk.com/dev/storage.set
    # http://vk.com/dev/storage.getKeys



    # # Написание сообщения пользователю с id=170968205 на стену:
    # rs = vk.method('wall.post', {'owner_id': '170968205', 'message': message})
    # print(rs)



    # # Написание сообщения пользователю с id=170968205 в диалог:
    # rs = vk.method('messages.send', {'user_id': '170968205', 'message': paste_url})
    # print(rs)



    # rs = vk.method('friends.get')
    # # rs = vk.method('friends.get', {'user_id': '59628698'})
    #
    # print("Всего друзей: {}".format(rs['count']))
    #
    # friends = [str(i) for i in rs['items']]
    #
    # rq_params = {
    #     'user_ids': ','.join(friends),
    #     'fields': 'relation'
    # }
    #
    # rs = vk.method('users.get', rq_params)
    # # print(rs)
    #
    # for i, f in enumerate(rs, 1):
    #     print(i, f)


    # ## Получение инфы о пользователе
    # # Получение инфы о текущем пользователе
    # rs = vk.method('users.get')
    #
    # # # Получение больше инфы о текущем пользователе
    # # rs = vk.method('users.get', {'fields': 'sex, city, online, screen_name'})
    #
    # # # Получение инфы о пользователе creeddevilmaycry
    # # rs = vk.method('users.get', {'user_ids': 'creeddevilmaycry'})
    # print(rs)


    # rs = vk.method('utils.getServerTime')
    # print(rs)


    # # # Получение инфы о пользователе
    # rs = vk.method('users.get', {'user_ids': 'arthur_iskuzhin'})
    # print(rs)


    # # # Получение инфы о пользователе или приложении по короткому имение
    # rs = vk.method('utils.resolveScreenName', {'screen_name': 'arthur_iskuzhin'})
    # print(rs)



    ## Печатаем текст последнего поста со стены
    # values = {
    #     'count': 1  # Получаем только один пост
    # }
    # response = vk.method('wall.get', values)  # Используем метод wall.get
    #
    # if response['items']:
    #     # Печатаем текст последнего поста со стены
    #     print(response['items'][0]['text'])


    # # Получение статуса
    # # http://vk.com/dev/status.get
    # rs = vk.method('status.get')
    # print(rs)
    #
    # # Установка статуса
    # # http://vk.com/dev/status.set
    # rs = vk.method('status.set', {'text': '*Задумал злобный план*'})
    # print(rs)


    # ## Написание сообщения на стену
    # # Написание сообщения себе на стену:
    # response = vk.method('wall.post', {'message': 'Hello World! Привет Мир!'})
    # print(response)
    #
    # # Написание сообщения пользователю с id=170968205 на стену:
    # response = vk.method('wall.post', {'owner_id': '170968205', 'message': 'Даров, чувак!'})
    # print(response)


    # rs = vk.method('wall.post', {
    #     'owner_id': '123810316',
    #     'message': 'vk_api!',
    #     # 'attachments': 'http://doghusky.ru/wp-content/uploads/2012/02/Siberian-Husky-Puppy-Photo_002-600x375.jpg',
    # })
    # print(rs)


    # rs = vk.method('wall.post', {
    #     # 'owner_id': '4033640',
    #     # 'message': 'Щенята!',
    #     'attachments': 'http://bash.im/quote/144613',
    # })
    # print(rs)