#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup


BASE_URL = "http://mywishlist.ru"
URL_GET_LOGIN = f"{BASE_URL}/login"
URL_POST_LOGIN = f"{BASE_URL}/login/login"


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"


def parse(rs: requests.Response) -> BeautifulSoup:
    return BeautifulSoup(rs.content, "html.parser")


def do_get(url: str, *args, **kwargs) -> tuple[requests.Response, BeautifulSoup]:
    rs = session.get(url, *args, **kwargs)
    rs.raise_for_status()

    return rs, parse(rs)


def do_post(url: str, *args, **kwargs) -> tuple[requests.Response, BeautifulSoup]:
    rs = session.post(url, *args, **kwargs)
    rs.raise_for_status()

    return rs, parse(rs)


@dataclass
class Api:
    login: str
    password: str
    last_rs: requests.Response = field(init=False, repr=False, default=None)
    last_soup: BeautifulSoup = field(init=False, repr=False, default=None)

    def auth(self):
        self.last_rs, self.last_soup = do_get(URL_GET_LOGIN)

        params = {
            "login[login]": self.login,
            "login[password]": self.password,
        }

        self.last_rs, self.last_soup = do_post(URL_POST_LOGIN, data=params)
        if "/me/" not in self.last_rs.url:
            raise Exception(f"Не получилось авторизоваться! {self.last_rs} - {self.last_rs.url}")


    def add_wish(self, title: str, img_path: str = None) -> int:
        url_get_add_wish = f"{BASE_URL}/me/{self.login}/wish/add"
        url_post_add_wish = url_get_add_wish + "?autocomplete=false"

        self.last_rs, self.last_soup = do_get(url_get_add_wish)

        params = {
            "wish[wish]": title,
            "wish[tags]": "",
            "wish[link]": "",
            "wish[picture_delete]": "0",
            "wish[picture_url]": "",
            "wish[price]": "",
            "wish[event]": "",
            "wish[post_current]": "",
            "wish[rating]": "2",
            "wish[visible]": "0",
            "wish[commentable]": "1",
        }

        files = []
        if img_path:
            files.append(
                ("wish[picture]", (img_path, open(img_path, "rb")))
            )

        self.last_rs, self.last_soup = do_post(
            url_post_add_wish,
            data=params,
            files=files
        )

        wish_el = self.last_soup.select_one('.pWishList .pWishData a[href*="/wish"]')
        if not wish_el:
            raise Exception("Не удалось найти желание!")

        return int(wish_el["href"].split("/")[-1])

    def set_wish_as_granted(self, wish_id: int, thanks: str = ""):
        url_get = f"{BASE_URL}/me/{self.login}/wish/check/{wish_id}"
        url_post = f"{BASE_URL}/me/{self.login}/wish/check_save/{wish_id}"

        self.last_rs, self.last_soup = do_get(url_get)

        params = {
            "wish[realized]": "false",
            "wish[thanks]": thanks,
        }

        self.last_rs, self.last_soup = do_post(
            url_post,
            data=params,
        )


if __name__ == "__main__":
    from datetime import datetime

    login = "9d57585a"
    password = "9d57585a-2643-4a2e-94da-b1068edfa087"

    api = Api(login, password)
    api.auth()

    wish_id = api.add_wish(
        title=f"Желание #{int(datetime.now().timestamp())}",
    )
    print(f"Добавлено желание #{wish_id}")

    wish_id = api.add_wish(
        title=f"Желание #{int(datetime.now().timestamp())}",
        img_path=r"..\..\pil_pillow__examples\blur\input.jpg",
    )
    print(f"Добавлено желание #{wish_id}")

    api.set_wish_as_granted(wish_id, thanks="Благодарности моем коту!")
    print(f"Желание #{wish_id} исполнено!")
