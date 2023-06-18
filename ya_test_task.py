#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests

from PySide.QtGui import *
from PySide.QtCore import *


URL_GET_ALL_STOPS = "http://mobileapps.krd.ru:9000/api/v2/db/stops"
URL_GET_STOP_ROUTE = "http://mobileapps.krd.ru:9000/api/v2/db/routes?stopId="


def get_all_stops():
    """
    Функция возращает все остановки.

    """

    rs = requests.get(URL_GET_ALL_STOPS)
    rs = rs.json()

    if rs["status"] != 200:
        raise Exception(rs["message"])

    return [(stop["id"], stop["name"]) for stop in rs["data"]]


def get_stop_route(stop_id):
    """
    Функция возвращает маршруты указанной остановки.

    :param stop_id:
    :return:
    """

    rs = requests.get(URL_GET_STOP_ROUTE + stop_id)
    rs = rs.json()

    if rs["status"] != 200:
        raise Exception(rs["message"])

    return [(stop["shortName"], stop["name"]) for stop in rs["data"]]


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.stop_list_widget = QListWidget()
        self.stop_list_widget.itemClicked.connect(self.item_stop_click)

        self.route_list_widget = QListWidget()

        self.fill_stops_list_button = QPushButton("Заполнить список остановок")
        self.fill_stops_list_button.clicked.connect(self.fill_list_stops)

        layout = QHBoxLayout()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.fill_stops_list_button)
        main_layout.addLayout(layout)

        layout.addWidget(self.stop_list_widget)
        layout.addWidget(self.route_list_widget)

        self.setLayout(main_layout)

    def fill_list_stops(self):
        self.route_list_widget.clear()
        self.stop_list_widget.clear()

        # Получаем список всех остановок
        for data in get_all_stops():
            stop_id, stop_name = data

            item = QListWidgetItem(stop_name)
            item.setData(Qt.UserRole, stop_id)

            self.stop_list_widget.addItem(item)

    def item_stop_click(self, item):
        stop_id = item.data(Qt.UserRole)

        self.route_list_widget.clear()

        # Получаем список маршрутов текущей остановки
        for data in get_stop_route(stop_id):
            short_name, name = data

            item = QListWidgetItem("{}: {}".format(short_name, name))
            self.route_list_widget.addItem(item)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    app.exec_()
