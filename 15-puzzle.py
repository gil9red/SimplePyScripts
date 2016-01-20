#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import random
    import sys

    from PySide.QtGui import *
    from PySide.QtCore import *

    app = QApplication(sys.argv)

    class Widget(QWidget):
        def __init__(self):
            super().__init__()

            self.setWindowTitle('15-puzzle')

            self.cell_size = 40
            self.resize(self.cell_size * 4, self.cell_size * 4)

            self.empty_value = 16
            self.matrix = None

            self.refill()

        def refill(self):
            seq = list(range(1, 16))
            random.shuffle(seq)

            # add empty cell
            seq.append(self.empty_value)

            self.matrix = [
                [seq.pop(0) for _ in range(4)]
                for _ in range(4)
            ]

        def mouseReleaseEvent(self, event):
            super().mouseReleaseEvent(event)

            pos = event.pos()
            x, y = pos.y() // self.cell_size, pos.x() // self.cell_size

            def get_cell_num(x, y):
                try:
                    return self.matrix[x][y], x, y
                except IndexError:
                    return None

            try:
                neig = [
                    get_cell_num(x-1, y),
                    get_cell_num(x+1, y),
                    get_cell_num(x, y-1),
                    get_cell_num(x, y+1),
                ]

                # Ищем пустую ячейку
                empty_cell = list(filter(lambda x: x is not None and x[0] == self.empty_value, neig))

                # Если соседняя клетка пустая
                if len(empty_cell) > 0:
                    # Значение текущей клетки
                    value = get_cell_num(x, y)[0]

                    # Значение пустой клетки, и ее координаты
                    empty_value, x2, y2 = empty_cell[0]

                    # Меняем клетки местами
                    self.matrix[x][y] = empty_value
                    self.matrix[x2][y2] = value

                    self.update()

                    # Матрицу переделываем в список
                    l = list()
                    for row in self.matrix:
                        l += row
                    # Последний элемент правильной собранной доски -- пустая ячейка, не учитываем ее
                    l.pop()

                    if l == list(range(1, 16)):
                        QMessageBox.information(self, 'Victory', 'Ok!')

            except IndexError:
                pass

        def paintEvent(self, event):
            super().paintEvent(event)

            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            painter.setPen(Qt.black)

            for i, row in enumerate(self.matrix):
                y = i * self.cell_size

                for j, num in enumerate(row):
                    x = j * self.cell_size

                    painter.setBrush(Qt.white if num == self.empty_value else Qt.yellow)
                    painter.drawRect(x, y, self.cell_size, self.cell_size)

                    text = str(num) if num != self.empty_value else ""
                    painter.drawText(x, y, self.cell_size, self.cell_size, Qt.AlignCenter, text)

    w = Widget()
    w.show()

    exit(app.exec_())
