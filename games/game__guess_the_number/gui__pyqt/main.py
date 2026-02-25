#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
import traceback
import sys

from PyQt5.Qt import *


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/907a596654aabb9948934b68b0f7b1fe392e23bd/qt__pyqt__pyside__pyqode/pyqt__QListWidget__Flow.py
class WrapListWidget(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setFlow(QListView.LeftToRight)
        self.setWrapping(True)
        self.setUniformItemSizes(True)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

        self.setWrapping(self.isWrapping())


class PageGuessWidget(QWidget):
    about_prev = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        self.lives = 10
        self.level = 0
        self.guess_number = 0

        self.pb_prev = QPushButton("Назад")
        self.pb_prev.clicked.connect(self.about_prev.emit)

        self.lbl_lives = QLabel()
        self.lbl_level = QLabel()

        self.lw_numbers = WrapListWidget()
        self.lw_numbers.itemClicked.connect(self._on_number_clicked)

        layout_header = QHBoxLayout()
        layout_header.addWidget(self.pb_prev)
        layout_header.addStretch()
        layout_header.addWidget(self.lbl_level)
        layout_header.addWidget(self.lbl_lives)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_header)
        main_layout.addWidget(self.lw_numbers)

        self.setLayout(main_layout)

        self._update_states()

    def _update_states(self) -> None:
        self.lbl_lives.setText(f"Жизней: {self.lives}")
        self.lbl_level.setText(f"Уровень: {self.level}")

    def start_game(self, level: int, lives=10) -> None:
        self.lives = lives
        self.level = level

        # Загадываем число
        self.guess_number = random.randint(1, self.level)

        self.lw_numbers.setEnabled(True)
        self.lw_numbers.clear()
        self.lw_numbers.addItems(map(str, range(1, level + 1)))

        self._update_states()

    def _on_number_clicked(self, item: QListWidgetItem) -> None:
        num = int(item.text())

        if self.guess_number == num:
            self.lw_numbers.item(num - 1).setBackground(Qt.green)
            QMessageBox.information(self, "Победа", "Ты угадал число!")
            self.lw_numbers.setEnabled(False)
            return

        elif self.guess_number > num:
            # Выделение от 0 индекса до указанного
            for i in range(num):
                self.lw_numbers.item(i).setBackground(Qt.red)

            QMessageBox.information(self, "Не угадал", "Загаданное число больше!")

        else:
            # Выделение красным от указанного индекса до конца
            for i in range(num - 1, self.lw_numbers.count()):
                self.lw_numbers.item(i).setBackground(Qt.red)

            QMessageBox.information(self, "Не угадал", "Загаданное число меньше!")

        self.lives -= 1
        if self.lives <= 0:
            QMessageBox.information(self, "Проигрыш", "У тебя закончили жизни!")
            self.lw_numbers.setEnabled(False)

        self._update_states()


class PageSelectLevelWidget(QWidget):
    about_select_level = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(QLabel("Выбор уровня сложности:"), 0, 0, 1, 2)
        self._add_levels([
            [25, 50],
            [75, 100],
            [125, 150],
            [175, 200],
        ])

        layout = QVBoxLayout()
        layout.addLayout(self.grid_layout)
        layout.addStretch()

        self.setLayout(layout)

    def _add_levels(self, levels) -> None:
        start_row = self.grid_layout.rowCount()

        for row, rows in enumerate(levels, start=start_row):
            for col, value in enumerate(rows):
                pb = QPushButton(str(value))
                pb.clicked.connect(
                    lambda checked, level=value: self.about_select_level.emit(level)
                )

                self.grid_layout.addWidget(pb, row, col)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Guess the number")

        self.stack_widget = QStackedWidget()

        self.page_select_level = PageSelectLevelWidget()
        self.page_select_level.about_select_level.connect(self._on_select_level)

        self.page_guess = PageGuessWidget()
        self.page_guess.about_prev.connect(
            lambda: self.stack_widget.setCurrentWidget(self.page_select_level)
        )

        self.stack_widget.addWidget(self.page_select_level)
        self.stack_widget.addWidget(self.page_guess)

        self.setCentralWidget(self.stack_widget)

    def _on_select_level(self, level: int) -> None:
        # Переключаемся на страницу с игрой
        self.stack_widget.setCurrentWidget(self.page_guess)

        self.page_guess.start_game(level)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
