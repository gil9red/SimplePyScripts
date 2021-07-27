#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Скрипт получает цитату с сайта bash.im и помещает ее на стену пользователя vk.com
The script receives a quote from the site bash.im and puts it on the wall by vk.com
"""


import time
import sys
from datetime import datetime

from root_config import DIR
from root_common import get_vk_session, vk_auth

# Для импортирования bash_im.py
sys.path.append(str(DIR.parent / 'html_parsing' / 'random_quote_bash_im'))

from bash_im import get_random_quotes


OWNER_ID = None


def main(login: str = None, password: str = None, owner_id: int = None, timeout: int = 60 * 60):
    if not login and not password:
        vk_session = get_vk_session()
    else:
        vk_session = vk_auth(login, password)

    vk = vk_session.get_api()

    while True:
        quote = get_random_quotes()[0]

        # Добавление сообщения на стену пользователя (owner_id это id пользователя)
        # Если не указывать owner_id, сообщения себе на стену поместится
        rs = vk.wall.post(
            owner_id=owner_id,
            message=quote.url + '\n\n' + quote.text,
        )

        cur_date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        print(f'{cur_date}: post_id: {rs["post_id"]}, quote: {quote.url}')

        time.sleep(timeout)


if __name__ == '__main__':
    main(owner_id=OWNER_ID)
