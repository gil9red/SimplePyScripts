__author__ = "ipetrash"


import argparse
from datetime import datetime, time


def main(namespace):
    args = namespace.parse_args()
    args.user = "Илья"
    if args.user:
        welcome = "Привет"

        current = datetime.now().time()
        if time(6) <= current < time(12):
            welcome = "Доброе утро"

        elif time(12) <= current < time(18):
            welcome = "Добрый день"

        elif time(18) <= current < time(23, 59, 59):
            welcome = "Добрый вечер"

        elif time(0) <= current < time(6):
            welcome = "Доброй ночи"

        print(f"{welcome}, {args.user}!")
    else:
        print("Привет, Python!")


def create_parser():
    parser = argparse.ArgumentParser(description="Hello World Example!")
    parser.add_argument("--user", type=str, help=" user name.")
    return parser


if __name__ == "__main__":
    parser = create_parser()
    main(parser)
