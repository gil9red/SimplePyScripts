#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class Window(Qt.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("draw__ellipse_board__chess_order__decrease")

    def paintEvent(self, event: Qt.QPaintEvent) -> None:
        painter = Qt.QPainter(self)
        painter.setRenderHint(Qt.QPainter.Antialiasing)
        painter.setPen(Qt.Qt.NoPen)
        painter.setBrush(Qt.Qt.black)

        original_w = 30

        w = original_w
        w_indent = w * 3
        h_indent = w * 2

        cols = self.width() // w + 1
        rows = 8

        y = 0

        for row in range(rows):
            for col in range(cols):
                x = col * w_indent
                if row % 2:
                    x += w_indent // 2

                pos = Qt.QPoint(x, y)

                painter.drawEllipse(pos, w, w)

            w -= 4
            y += h_indent


if __name__ == "__main__":
    app = Qt.QApplication([])

    w = Window()
    w.resize(450, 450)
    w.show()

    app.exec()
