#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup

from common import session


@dataclass
class Wish:
    id: int
    user: str
    title: str
    created_at: datetime
    img_url: str

    @classmethod
    def parse_from(cls, url: str) -> Optional["Wish"]:
        rs = session.get(url)
        rs.raise_for_status()

        soup = BeautifulSoup(rs.content, "html.parser")

        user_el = soup.select_one(".pWishFull .pProfile a")
        if not user_el:
            return None

        created_at_str = soup.select_one(".pWishData .pPostText .Date").get_text(strip=True)
        created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M")

        img_el = soup.select_one(".pWishFull noindex > a > img[src]")
        img_url = img_el["src"] if img_el else ""

        return cls(
            id=int(url.split("/")[-1]),
            user=user_el.get_text(strip=True),
            title=soup.select_one(".pWishData h5").get_text(strip=True),
            created_at=created_at,
            img_url=img_url,
        )


if __name__ == "__main__":
    wish = Wish.parse_from("http://mywishlist.ru/wish/8888")
    print(wish)
    # Wish(id=8888, user='Olesialirika', title='стать спутницей жизни для того,кого люблю', created_at=datetime.datetime(2006, 9, 12, 21, 47), img_url='/pic/i/wish/300x300/000/008/888.gif')

    wish = Wish.parse_from("http://mywishlist.ru/wish/446")
    print(wish)
    # None
