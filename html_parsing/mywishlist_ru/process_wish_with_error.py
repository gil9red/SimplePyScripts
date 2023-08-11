#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collect_wishes import Wish, WishInfo, get_wish_data


def run():
    for wish in Wish.select().where(Wish.error.is_null(False)):
        try:
            wish_info = WishInfo.parse_from(wish.id)
            if not wish_info:
                print(f"Желание #{wish.id} все еще неуспешно парсится")
                continue

            wish_data = get_wish_data(wish_info)

            wish.user = wish_data["user"]
            wish.user_url = wish_data["user_url"]
            wish.title = wish_data["title"]
            wish.created_at = wish_data["created_at"]
            wish.img_url = wish_data["img_url"]
            wish.error = None

            wish.save()

            print(f"Желание #{wish.id} успешно обработано и сохранено:\n    {wish}\n")

        except Exception as e:
            print(f"Осталась ошибка: {e}")


if __name__ == "__main__":
    run()
