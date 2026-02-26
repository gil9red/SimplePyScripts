#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import logging
import traceback
import sys

from collections import OrderedDict
from datetime import datetime
from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup

from qtpy.QtWidgets import *
from qtpy.QtGui import *
from qtpy.QtCore import *


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    logging.critical(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


URL = "http://www.jazzcinema.ru/schedule/"


class Movie:
    def __init__(self, border) -> None:
        a = border.select_one(".movie .title > a")
        self.movie_url = urljoin(URL, a["href"])

        self.title = a["title"]

        self.genre = border.select_one(".genre")
        if self.genre:
            self.genre = self.genre.text

        self.seanses = OrderedDict()
        for seanse in border.select(".seanses li"):
            time = seanse.select_one("a").text
            price = seanse.select_one(".price").text
            self.seanses[time] = price

        movie_info = border.next_sibling

        self.annotation = movie_info.select_one(".text").text.strip()

        img_url = movie_info.select_one(".poster img")["src"]
        self.img_url = urljoin(URL, img_url)

        # Начало и конец проката
        self.start_rentals = None
        self.end_rentals = None

        self.country = None
        self.producer = None
        self.actors = None
        self.duration = None
        self.age_restrictions = movie_info.select_one(".text.age-count").text.strip()

        for td in movie_info.select("table td"):
            key = td.text.strip()
            if key.endswith(":"):
                value = td.next_sibling.text.strip()

                if "Начало проката:" == key:
                    self.start_rentals = value
                elif "Окончание проката:" == key:
                    self.end_rentals = value
                elif "Страна:" == key:
                    self.country = value
                elif "Режиссёр:" == key:
                    self.producer = value
                elif "В ролях:" == key:
                    self.actors = value
                elif "Продолжительность:" == key:
                    self.duration = value


class MovieInfoWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # TODO: можно и видео добавить
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)

        self.setLayout(layout)

    def set_movie(self, movie) -> None:
        data = dict()

        # Скачивание обложки и получени base64
        with urlopen(movie.img_url) as f:
            img_base64 = base64.standard_b64encode(f.read()).decode("utf-8")
            data["img_url"] = "data:image/png;base64," + img_base64

        seanses_table = "<table>"

        for time, price in movie.seanses.items():
            seanses_table += (
                f"<tr><td>{time}&nbsp;&nbsp;&nbsp;&nbsp;</td><td>{price}</td></tr>"
            )

        seanses_table += "</table>"

        data["seanses_table"] = seanses_table

        html = """
<html>
    <head>
        <meta charset="utf-8">
    </head>

    <body>
        <table cellpadding="10">
            <tr>
                <td><img src="{img_url}"/></td>
                <td>
                    <a href="{0.movie_url}">{0.title}</a>
                    <br>

                    <table>
                        <tr><td>Начало проката:</td><td>{0.start_rentals}</td></tr>
                        <tr><td>Окончание проката:</td><td>{0.end_rentals}</td></tr>
                        <tr><td>Жанр:</td><td>{0.genre}</td></tr>
                        <tr><td>Страна:</td><td>{0.country}</td></tr>
                        <tr><td>Режиссёр:</td><td>{0.producer}</td></tr>
                        <tr><td>В ролях:</td><td colspan="3">{0.actors}</td></tr>
                        <tr><td>Возрастные ограничения:</td><td>{0.age_restrictions}</td></tr>
                        <tr><td>Продолжительность:</td><td>{0.duration}</td></tr>
                        <tr><td colspan="4">Аннотация:<br>{0.annotation}</td></tr>
                        <tr></tr>

                        <tr>
                            <td colspan="2">Сеансы:
                            {seanses_table}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>
        """.format(
            movie, **data
        )

        self.browser.setHtml(html)


class SchedulerMoviePage(QWidget):
    def __init__(self, schedule) -> None:
        super().__init__()

        self.schedule_date_str = datetime.strptime(
            schedule["rel"], "calendar-%Y-%m-%d-schedule"
        ).strftime("%d/%m/%Y")

        self.movie_list_widget = QListWidget()
        self.movie_list_widget.currentItemChanged.connect(
            lambda current, previous: self.movie_info.set_movie(
                current.data(Qt.UserRole)
            )
        )

        self.movie_info = MovieInfoWidget()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.movie_list_widget)
        splitter.addWidget(self.movie_info)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        # Получение фильмов в текущей вкладке (в каждой вкладке будет свой список фильмов на день)
        for border in schedule.select(".border"):
            movie = Movie(border)

            item = QListWidgetItem(movie.title)
            item.setData(Qt.UserRole, movie)
            self.movie_list_widget.addItem(item)

        self.movie_list_widget.setCurrentRow(0)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("show_schedule_gui.py")

        self.tab_widget = QTabWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Расписание фильмов на:"))
        layout.addWidget(self.tab_widget)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def load(self) -> None:
        with urlopen(URL) as f:
            root = BeautifulSoup(f.read(), "lxml")

            # Список расписаний
            schedule_list = root.select(".schedule")

            # Проходим по списку расписаний
            for schedule in schedule_list:
                # Если фильмов нет
                if not schedule.select(".border"):
                    continue

                tab = SchedulerMoviePage(schedule)
                self.tab_widget.addTab(tab, tab.schedule_date_str)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(900, 500)
    mw.show()
    mw.load()

    app.exec()
