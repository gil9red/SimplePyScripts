#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import BASE_URL, do_get


def get_last_id_wish(safe: bool = False) -> int | None:
    try:
        _, soup = do_get(BASE_URL)
        wish_url = soup.select_one(".pWishList .pWishLite a[href]")["href"]
        return int(wish_url.split("/")[-1])
    except Exception as e:
        if safe:
            return
        raise e


if __name__ == "__main__":
    last_id = get_last_id_wish()
    print(last_id)
    # 10320355

    from get_wish_info import Wish
    print(Wish.parse_from(last_id))
    # Wish(id=10320355, user='Wicked Red Fish', title='PREDUBEZHDAI butter body', created_at='2023-08-08 23:50', img_url='/pic/i/wish/300x300/010/320/355.jpeg')
