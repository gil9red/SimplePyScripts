#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Пример отправки сообщения самому себе
"""


from vk_api.utils import get_random_id
from root_common import get_vk_session, get_logger


def send_message(vk, text: str, user_id: int = None):
    values = {
        'user_id': user_id,
        'message': text,
        'random_id': get_random_id(),
    }

    logger.debug(f'Execute vk method messages.send with values: {values}')
    result = vk.messages.send(values=values)
    logger.debug(f'Result: {result}')

    return result


logger = get_logger('selfie_send')

# Id пользователя, которому пошлем сообщение
USER_ID = None


if __name__ == '__main__':
    try:
        logger.debug('Vk authorization')
        vk_session = get_vk_session()
        vk = vk_session.get_api()

        send_message(vk, 'Hello! Привет!\nYahoo!', USER_ID)

    except Exception as e:
        logger.exception("Error:")
