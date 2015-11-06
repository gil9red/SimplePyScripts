#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtGui import *
from PySide.QtCore import *

from random import randint
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    class Widget(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle('Widget')

            self.cell_size = 20
            self.row_count = 9
            self.column_count = 9

            self.x_highlight_cell = -1
            self.y_highlight_cell = -1

            # Заполняем матрицу случайными числами от 0 до 9
            self.matrix = list()
            for i in range(self.row_count):
                row = list()
                self.matrix.append(row)

                for j in range(self.column_count):
                    row.append(randint(0, 9))

            self.setMouseTracking(True)

        def mouseMoveEvent(self, event):
            pos = event.pos()

            self.x_highlight_cell = pos.x() // self.cell_size
            self.y_highlight_cell = pos.y() // self.cell_size

            self.update()

        def paintEvent(self, event):
            painter = QPainter(self)

            # Если индекс ячейки под курсором валидный
            if 0 <= self.x_highlight_cell < self.row_count and 0 <= self.y_highlight_cell < self.column_count:
                # Выделение всего столбца и строки пересекающих ячейку под курсором
                painter.save()
                painter.setBrush(Qt.lightGray)

                # Выделение строки
                for i in range(self.row_count):
                    painter.drawRect(i * self.cell_size,
                                     self.y_highlight_cell * self.cell_size,
                                     self.cell_size,
                                     self.cell_size)

                # Выделение столбца
                for j in range(self.column_count):
                    painter.drawRect(self.x_highlight_cell * self.cell_size,
                                     j * self.cell_size,
                                     self.cell_size,
                                     self.cell_size)

                painter.restore()

                # Выделение ячейки под курсором
                painter.save()
                painter.setBrush(Qt.yellow)
                painter.drawRect(self.x_highlight_cell * self.cell_size,
                                 self.y_highlight_cell * self.cell_size,
                                 self.cell_size,
                                 self.cell_size)
                painter.restore()

            # Рисование цифр в ячейки таблицы
            for i in range(self.row_count):
                for j in range(self.column_count):
                    num = self.matrix[i][j]

                    x = i * self.cell_size
                    y = j * self.cell_size
                    w, h = self.cell_size, self.cell_size
                    painter.drawText(x, y, w, h, Qt.AlignCenter, str(num))

            # Рисование сетки таблицы
            y1, y2 = 0, 0

            for i in range(self.row_count + 1):
                painter.drawLine(0, y1, self.cell_size * self.column_count, y2)
                y1 += self.cell_size
                y2 += self.cell_size

            x1, x2 = 0, 0

            for i in range(self.column_count + 1):
                painter.drawLine(x1, 0, x2, self.cell_size * self.row_count)
                x1 += self.cell_size
                x2 += self.cell_size

    w = Widget()
    w.resize(200, 200)
    w.show()

    sys.exit(app.exec_())
