#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from datetime import datetime, date

from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup


if __name__ == "__main__":
    url = "http://www.jazzcinema.ru/"

    with urlopen(url) as f:
        root = BeautifulSoup(f.read(), "lxml")

        # Список расписаний
        schedule_list = root.select(".schedule")

        today = date.today()
        today_found = False

        # Проходим по списку и ищем расписание на текущую дату
        for schedule in schedule_list:
            schedule_date = datetime.strptime(
                schedule["rel"], "calendar-%Y-%m-%d-schedule"
            ).date()
            schedule_date_str = schedule_date.strftime("%d/%m/%Y")

            border_list = schedule.select(".border")
            if schedule_date == today and border_list:
                today_found = True
                print(f"Расписание фильмов на сегодня {schedule_date_str}:")

                # Получение фильмов в текущей вкладке (по идеи, текущая вкладка -- текущий день)
                for border in border_list:
                    a = border.select_one(".movie .title > a")
                    url = urljoin(url, a["href"])
                    print(f'    "{a["title"]}": {url}')
                    print(f"        {border.select_one('.genre').text}")

                    for seanse in border.select(".seanses li"):
                        time = seanse.select_one("a").text
                        price = seanse.select_one(".price").text
                        print(f"        {time} : {price}")

                    print()

        if not today_found:
            print(f"Фильмов на сегодня ({today.strftime('%d/%m/%Y')}) нет")
