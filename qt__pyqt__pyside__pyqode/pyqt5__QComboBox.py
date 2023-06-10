#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.Qt import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.tb_result = QTextBrowser()

        self.cb_pets = QComboBox()
        self.cb_pets.currentIndexChanged.connect(self._on_pet_changed)
        self.cb_pets.addItem("Собаки", userData="dogs")
        self.cb_pets.addItem("Коты", userData="cats")

        layout = QVBoxLayout()
        layout.addWidget(self.cb_pets)
        layout.addWidget(self.tb_result)

        self.setLayout(layout)

    def _on_pet_changed(self, index):
        # print(index)                          # 0
        # print(self.cb_pets.itemText(index))   # Собаки
        # print(self.cb_pets.itemData(index))   # dogs
        # print()
        # print(self.cb_pets.currentIndex())    # 0
        # print(self.cb_pets.currentText())     # Собаки
        # print(self.cb_pets.currentData())     # dogs
        data = self.cb_pets.itemData(index)

        if data == "cats":
            text = "Вы любите кошек"
        elif data == "dogs":
            text = "Вы любите собак"
        else:
            text = ""

        self.tb_result.setHtml(text)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
