#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt

from PyQt5.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QFormLayout,
    QLabel,
)
from PyQt5.QtCore import Qt


class ListItem(QFrame):
    def __init__(
        self,
        host: str,
        port: int,
        status: str = "Not checked!",
        last_check_time: dt.datetime = None,
    ) -> None:
        super().__init__()

        if not last_check_time:
            last_check_time = dt.datetime.now()

        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Plain)

        self.label_address = QLabel(f"{host}:{port}")
        self.label_status = QLabel(status)
        self.label_last_check_time = QLabel(
            last_check_time.strftime("%d/%m/%Y %H:%M:%S")
        )

        main_layout = QFormLayout(self)
        main_layout.addRow("Address:", self.label_address)
        main_layout.addRow("Status:", self.label_status)
        main_layout.addRow("Last check time:", self.label_last_check_time)

        self.setFixedHeight(self.sizeHint().height())


def add_item(list_widget: QListWidget, host: str, port: int) -> None:
    widget = ListItem(host, port)

    item = QListWidgetItem()
    item.setSizeHint(widget.sizeHint())
    item.setData(Qt.UserRole, widget)

    list_widget.addItem(item)
    list_widget.setItemWidget(item, widget)


if __name__ == "__main__":
    app = QApplication([])

    list_widgets = QListWidget()
    list_widgets.resize(350, 240)
    list_widgets.setSpacing(2)

    list_widgets.itemClicked.connect(lambda item: print(item.data(Qt.UserRole)))

    add_item(list_widgets, "127.0.0.1", 161)
    add_item(list_widgets, "192.168.0.0", 161)
    for i in range(1, 10 + 1):
        add_item(list_widgets, "127.0.0.1", 161 + i)

    list_widgets.show()

    app.exec()
