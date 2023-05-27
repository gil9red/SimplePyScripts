#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime

from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup


if __name__ == "__main__":
    url = "http://www.jazzcinema.ru/"

    with urlopen(url) as f:
        root = BeautifulSoup(f.read(), "lxml")

        # Список расписаний
        schedule_list = root.select(".schedule")

        for schedule in schedule_list:
            schedule_date = datetime.strptime(
                schedule["rel"], "calendar-%Y-%m-%d-schedule"
            ).strftime("%d/%m/%Y")
            border_list = schedule.select(".border")

            # Если фильмов нет
            if not border_list:
                continue

            print(f"Расписание фильмов за {schedule_date}:")

            # Получение фильмов в текущей вкладке (по идеи, текущая вкладка -- текущий день)
            for border in schedule.select(".border"):
                a = border.select_one(".movie .title > a")
                url = urljoin(url, a["href"])
                print(f'    "{a["title"]}": {url}')
                genre = border.select_one(".genre")
                if genre:
                    print(f"        {genre.text}")

                for seanse in border.select(".seanses li"):
                    time = seanse.select_one("a").text
                    price = seanse.select_one(".price").text
                    print(f"        {time} : {price}")

                print()
