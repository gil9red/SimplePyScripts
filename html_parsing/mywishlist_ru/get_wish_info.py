#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, asdict
from typing import Optional

from common import BASE_URL, do_get


URL_WISH = f"{BASE_URL}/wish"


@dataclass
class Wish:
    id: int
    user: str
    user_url: str
    title: str
    created_at: str
    img_url: str

    @classmethod
    def parse_from(cls, wish_id: int) -> Optional["Wish"]:
        url = f"{URL_WISH}/{wish_id}"

        _, soup = do_get(url)

        user_el = soup.select_one(".pWishFull .pProfile a")
        if not user_el:
            return None

        created_at_el = soup.select_one(".pWishData .pPostText .Date")
        created_at_str = created_at_el.get_text(strip=True)

        img_el = soup.select_one(".pWishFull noindex > a > img[src]")
        img_url = img_el["src"] if img_el else ""

        return cls(
            id=wish_id,
            user=user_el.get_text(strip=True),
            user_url=user_el["href"],
            title=soup.select_one(".pWishData h5").get_text(strip=True),
            created_at=created_at_str,
            img_url=img_url,
        )

    def as_dict(self) -> dict:
        return asdict(self)


if __name__ == "__main__":
    wish = Wish.parse_from(8888)
    print(wish)
    # Wish(id=8888, user='Olesialirika', user_url='/wishlist/olesialirika', title='стать спутницей жизни для того,кого люблю', created_at='2006-09-12 21:47', img_url='/pic/i/wish/300x300/000/008/888.gif')

    wish = Wish.parse_from(446)
    print(wish)
    # None
