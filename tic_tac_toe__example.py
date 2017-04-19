#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *

except:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Матрица 3 на 3
        self._board_tic_tac_toe = [[None for _ in range(3)] for _ in range(3)]

        self._size_cell = 80

        # If True -- X else -- O
        self._current_figure_flag = True

    def _check_win(self):
        b = self._board_tic_tac_toe
        win_X = False
        win_O = False

        seq_X = ['X', 'X', 'X']
        seq_O = ['O', 'O', 'O']

        if not win_X and not win_O:
            # Построчная проверка
            for row in b:
                if row == seq_X:
                    win_X = True
                    break

                if row == seq_O:
                    win_O = True
                    break

        if not win_X and not win_O:
            # Проверка в столбиках
            for i in range(3):
                col = [b[0][i], b[1][i], b[2][i]]

                if col == seq_X:
                    win_X = True
                    break

                if col == seq_O:
                    win_O = True
                    break

        if not win_X and not win_O:
            # Проверка по диагонали
            for i in range(3):
                diag_1 = [b[0][0], b[1][1], b[2][2]]
                diag_2 = [b[2][0], b[1][1], b[0][2]]

                if diag_1 == seq_X or diag_2 == seq_X:
                    win_X = True
                    break

                if diag_1 == seq_O or diag_2 == seq_O:
                    win_O = True
                    break

        if win_X:
            QMessageBox.information(self, 'Winner', 'Win X')
            return

        if win_O:
            QMessageBox.information(self, 'Winner', 'Win O')
            return

    def mouseReleaseEvent(self, e):
        # Определяем позицию клика
        i = e.pos().y() // self._size_cell
        j = e.pos().x() // self._size_cell

        # Выход за пределы массива
        if i >= 3 or j >= 3:
            return

        self._board_tic_tac_toe[i][j] = 'X' if self._current_figure_flag else 'O'
        self._current_figure_flag = not self._current_figure_flag

        # Перерисовка, вызов paintEvent
        self.update()

        self._check_win()

    def paintEvent(self, e):
        painter = QPainter(self)

        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)

        for i in range(len(self._board_tic_tac_toe)):
            row = self._board_tic_tac_toe[i]

            for j in range(len(row)):
                x = j * self._size_cell
                y = i * self._size_cell
                w = self._size_cell
                h = self._size_cell

                painter.drawRect(x, y, w, h)

                painter.save()
                painter.setFont(QFont('Arial', 16))

                value = self._board_tic_tac_toe[i][j]
                painter.setPen(Qt.blue if value == 'X' else Qt.red)

                painter.drawText(x, y, w, h, Qt.AlignCenter, value)

                painter.restore()


if __name__ == '__main__':
    app = QApplication([])

    w = Window()
    w.show()

    app.exec()
