#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests

try:
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
except:
    from PySide.QtGui import *
    from PySide.QtCore import *

a = QApplication([])


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.lw_dep = QListWidget()
        self.lw_dep.clicked.connect(self.fill_kaf)

        self.lw_kaf = QListWidget()
        self.lw_kaf.clicked.connect(self.fill_stu)

        self.lw_stu = QListWidget()

        layout = QHBoxLayout()
        layout.addWidget(self.lw_dep)
        layout.addWidget(self.lw_kaf)
        layout.addWidget(self.lw_stu)

        self.setLayout(layout)

    def fill(self):
        self.lw_dep.clear()
        rs = requests.get(
            "http://magtu.ru/modules/mod_reiting/mobile.php?action=get_all_department"
        )
        rs.raise_for_status()

        for dep in rs.json():
            id_dep = list(dep.keys())[0]
            name = dep[id_dep]

            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, id_dep)
            self.lw_dep.addItem(item)

    def fill_kaf(self, item_dep):
        self.lw_kaf.clear()

        id_dep = item_dep.data(Qt.UserRole)
        rs = requests.get(
            f"http://magtu.ru/modules/mod_reiting/mobile.php?action=get_spec_by_depart&depart_kod={id_dep}"
        )
        rs.raise_for_status()

        for kaf in rs.json():
            id_kaf = list(kaf.keys())[0]
            name = kaf[id_kaf]

            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, id_kaf)
            self.lw_kaf.addItem(item)

    def fill_stu(self, item_kaf):
        self.lw_stu.clear()

        id_kaf = item_kaf.data(Qt.UserRole)
        rs = requests.get(
            f"http://magtu.ru/modules/mod_reiting/mobile.php?action=get_reiting&spec_kod={id_kaf}"
        )
        rs.raise_for_status()

        for stud in rs.json():
            name = stud[0]

            item = QListWidgetItem(name)
            self.lw_stu.addItem(item)


w = Widget()
w.show()
w.fill()

a.exec_()
