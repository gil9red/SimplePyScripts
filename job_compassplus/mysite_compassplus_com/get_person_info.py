#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from common import URL, do_get


@dataclass
class Person:
    name: str
    position: str
    department: str
    img_url: str
    location: str
    birthday: str


def get_person_info(name: str, domain: str = "CP") -> Person | None:
    url = URL.format(fr"{domain}\{username}")

    rs = do_get(url)
    soup = BeautifulSoup(rs.content, "html.parser")

    img_el = soup.select_one("#ctl00_PictureUrlImage")
    if not img_el:  # Сайт не умеет показывать 404 при отсутствующем пользователе
        return

    return Person(
        name=name,
        position=soup.select_one("#ProfileViewer_ValueTitle").get_text(strip=True),
        department=soup.select_one("#ProfileViewer_ValueDepartment").get_text(strip=True),
        img_url=urljoin(rs.url, img_el["src"]),
        location=soup.select_one('div[id *= "_ProfileViewer_SPS-Location"] > .ms-profile-detailsValue').get_text(strip=True),
        birthday=soup.select_one('div[id *= "_ProfileViewer_SPS-Birthday"] > .ms-profile-detailsValue').get_text(strip=True),
    )


if __name__ == "__main__":
    username = "ipetrash"

    info = get_person_info(username)
    print(info)
    # Person(name='ipetrash', position='Senior Software Engineer', department='TX SPD, Application Platforms Division', img_url='https://portal.compassplus.com/my/User%20Photos/Profile%20Pictures/ipetrash.jpg', location='Magnitogorsk', birthday='August 18')
