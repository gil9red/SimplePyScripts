#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from urllib.request import urlopen

from collections import OrderedDict

from bs4 import BeautifulSoup

URL = 'http://www.jazzcinema.ru/'


class Movie:
    def __init__(self, border):
        a = border.select_one('.movie .title > a')
        self.movie_url = urljoin(URL, a['href'])

        self.title = a['title']

        genre = border.select_one('.genre')
        if genre:
            self.genre = genre.text

        self.seanses = OrderedDict()
        for seanse in border.select('.seanses'):
            time = seanse.select_one('a').text
            price = seanse.select_one('.price').text
            self.seanses[time] = price

        movie_info = border.next_sibling

        img_url = movie_info.select_one('.poster img')["src"]
        self.img_url = urljoin(URL, img_url)

        # Начало и конец проката
        self.start_rentals = None
        self.end_rentals = None

        self.country = None
        self.producer = None
        self.actors = None
        self.duration = None

        for td in movie_info.select('table td'):
            key = td.text.strip()
            if key.endswith(":"):
                value = td.next_sibling.text.strip()

                if 'Начало проката:' == key:
                    self.start_rentals = value
                elif 'Окончание проката:' == key:
                    self.end_rentals = value
                elif 'Страна:' == key:
                    self.country = value
                elif 'Режиссёр:' == key:
                    self.producer = value
                elif 'В ролях:' == key:
                    self.actors = value
                elif 'Продолжительность:' == key:
                    self.duration = value

# Начало проката:
# Окончание проката:
# Страна:
# Режиссёр:
# В ролях:
# Возрастные ограничения:
# Продолжительность:


if __name__ == '__main__':
    with urlopen(URL) as f:
        root = BeautifulSoup(f.read(), 'lxml')

        # Список расписаний
        schedule_list = root.select('.schedule')

        from datetime import datetime, date
        today = date.today()

        today_found = False

        # Проходим по списку и ищем расписание на текущую дату
        for schedule in schedule_list:
            schedule_date = datetime.strptime(schedule['rel'], 'calendar-%Y-%m-%d-schedule').date()
            schedule_date_str = schedule_date.strftime('%d/%m/%Y')

            # Получение фильмов в текущей вкладке (по идеи, текущая вкладка -- текущий день)
            for border in schedule.select('.border'):
                movie = Movie(border)
                print(movie.title)
                quit()
