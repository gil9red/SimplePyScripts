#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urljoin
from urllib.request import urlopen

from datetime import datetime

from collections import OrderedDict

from bs4 import BeautifulSoup

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)

    import traceback
    text += ''.join(traceback.format_tb(tb))

    import logging
    logging.critical(text)
    QMessageBox.critical(None, 'Error', text)
    quit()

import sys
sys.excepthook = log_uncaught_exceptions


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


class MovieInfoWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.browser = QTextBrowser()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)

        self.setLayout(layout)

    def set_movie(self, movie):
        html = """
<html>
    <head>
        <meta charset="utf-8">
    </head>

    <body>
        {0.title}
    </body>
</html>
        """.format(movie)
        print(html)

        self.browser.setHtml(html)


class SchedulerMoviePage(QWidget):
    def __init__(self, schedule):
        super().__init__()

        self.schedule_date_str = datetime.strptime(schedule['rel'], 'calendar-%Y-%m-%d-schedule').strftime('%d/%m/%Y')

        self.movie_list_widget = QListWidget()
        self.movie_list_widget.currentItemChanged.connect(lambda current, previous:
                                                          self.movie_info.set_movie(current.data(Qt.UserRole)))

        self.movie_info = MovieInfoWidget()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.movie_list_widget)
        splitter.addWidget(self.movie_info)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        # Получение фильмов в текущей вкладке (по идеи, текущая вкладка -- текущий день)
        for border in schedule.select('.border'):
            movie = Movie(border)

            item = QListWidgetItem(movie.title)
            item.setData(Qt.UserRole, movie)
            self.movie_list_widget.addItem(item)

        self.movie_list_widget.setCurrentRow(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('show_schedule_gui.py')

        self.tab_widget = QTabWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Расписание фильмов за:'))
        layout.addWidget(self.tab_widget)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def load(self):
        with urlopen(URL) as f:
            root = BeautifulSoup(f.read(), 'lxml')

            # Список расписаний
            schedule_list = root.select('.schedule')

            # Проходим по списку расписаний
            for schedule in schedule_list:
                # Если фильмов нет
                if not schedule.select('.border'):
                    continue

                tab = SchedulerMoviePage(schedule)
                self.tab_widget.addTab(tab, tab.schedule_date_str)


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.show()
    mw.load()

    app.exec()
