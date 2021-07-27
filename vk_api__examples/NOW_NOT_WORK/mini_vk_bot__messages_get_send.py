#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# NOTE: see https://github.com/gil9red/mini_vk_bot


import time
import traceback

from root_common import get_vk_session


# TODO: обрабатывать не последнее полученное сообщение, а пачку, например 100


if __name__ == '__main__':
    vk_session = get_vk_session()

    command_prefix = 'Бот, '

    # Ограничение бота, чтобы он не отвечал на свои же сообщения
    # Для снятие ограничения: bot_user_id = None
    rs = vk_session.method('users.get')
    bot_user_id = rs[0]['id']

    last_message_bot_id = None

    messages_get_values = {
        'out': 0,
        'count': 1,
        'time_offset': 60,
        'version': '5.67'
    }

    while True:
        try:
            rs = vk_session.method('messages.get', messages_get_values)
            print(rs)

            # Если ничего не пришло
            if not rs['items']:
                continue

            message_id = rs['items'][0]['id']
            from_user_id = rs['items'][0]['user_id']
            message = rs['items'][0]['body']

            # Не будем отвечать на собственное сообщение
            if from_user_id == bot_user_id:
                continue

            # Бот реагирует только на сообщения, начинающиеся с префикса
            if not message.lower().startswith(command_prefix.lower()):
                continue

            print(f'    From user #{from_user_id}, message (#{message_id}): "{message}"')
            command = message[len(command_prefix):]

            message = f'Получена команда: {command!r}'
            last_message_bot_id = vk_session.method('messages.send', {'user_id': from_user_id, 'message': message})

            messages_get_values['last_message_id'] = last_message_bot_id

        except Exception as e:
            print('Error:', traceback.format_exc())

        finally:
            time.sleep(3)
