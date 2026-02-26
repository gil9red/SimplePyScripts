#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback

from PyQt5.Qt import *


def log_uncaught_exceptions(ex_cls, ex, tb) -> None:
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class FlowWidget(QWidget):
    def __init__(self, length=25, cell_size=50, cell_font=QFont("Arial", 10)) -> None:
        super().__init__()

        self.cell_size = cell_size
        self.cell_font = cell_font

        self.column_count = 10
        self.items = list(range(1, length + 1))

    def minimumSizeHint(self):
        try:
            # + 1 -- толщина рамки
            height = (len(self.items) // self.column_count + 1) * self.cell_size + 1
            return QSize(self.minimumWidth(), height)

        except ZeroDivisionError:
            return super().minimumSizeHint()

    def minimumSize(self):
        return self.minimumSizeHint()

    def showEvent(self, event) -> None:
        super().showEvent(event)

        self.updateGeometry()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

        self.column_count = self.width() // self.cell_size

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        painter.setFont(self.cell_font)

        for index, num in enumerate(self.items):
            num = str(num)

            # Превращаем индекс в координаты
            row = index // self.column_count
            col = index % self.column_count

            x = col * self.cell_size
            y = row * self.cell_size
            w, h = self.cell_size, self.cell_size

            painter.drawRect(x, y, w, h)
            painter.drawText(x, y, w, h, Qt.AlignCenter, num)


if __name__ == "__main__":
    app = QApplication([])

    simple = FlowWidget()
    simple.setWindowTitle("Simple")
    simple.resize(300, 300)
    simple.show()

    def get_QScrollArea_with_FlowWidget(length):
        scroll = QScrollArea()
        scroll.setWidget(FlowWidget(length))
        scroll.setWidgetResizable(True)
        return scroll

    mw = QTabWidget()
    mw.setWindowTitle("More examples")
    mw.addTab(get_QScrollArea_with_FlowWidget(25), "25")
    mw.addTab(get_QScrollArea_with_FlowWidget(100), "100")
    mw.addTab(get_QScrollArea_with_FlowWidget(250), "250")
    mw.addTab(get_QScrollArea_with_FlowWidget(500), "500")
    mw.addTab(get_QScrollArea_with_FlowWidget(1000), "1000")
    mw.resize(800, 500)
    mw.show()

    app.exec()
