#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт получает цитату с сайта bash.im и помещает ее на стену пользователя vk.com
The script receives a quote from the site bash.im and puts it on the wall by vk.com
"""


import argparse
import sys

from wall_post__bash_quotes import main


def create_parser():
    parser = argparse.ArgumentParser(
        description="The script receives a quote from the site bash.im "
        "and puts it on the wall by vk.com"
    )
    parser.add_argument("login", help="Login from which the message will be sent.")
    parser.add_argument("psw", help="User password.")
    parser.add_argument(
        "owner_id", type=int, nargs="?", const=1, help="ID on who will get the message."
    )
    parser.add_argument(
        "-timeout",
        type=int,
        default=3600,
        help="The frequency of sending messages in seconds." "\nDefault 3600 sec.",
    )
    return parser


if __name__ == "__main__":
    parser = create_parser()

    # Если не указаны параметры, выводим справку и выходим
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    main(
        login=args.login,
        password=args.psw,
        owner_id=args.owner_id,
        timeout=args.timeout,
    )
