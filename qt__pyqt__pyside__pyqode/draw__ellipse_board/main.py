#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class CellWidget(Qt.QWidget):
    def __init__(self):
        super().__init__()

        self.ball_size = 100

    def paintEvent(self, event: Qt.QPaintEvent):
        painter = Qt.QPainter(self)
        painter.setRenderHint(Qt.QPainter.Antialiasing)
        painter.setPen(Qt.Qt.NoPen)
        painter.setBrush(Qt.Qt.black)

        w = self.ball_size

        cols = self.width() // w + 1
        rows = self.height() // w + 1

        for row in range(rows):
            for col in range(cols):
                painter.drawEllipse(col * w, row * w, w, w)


class Window(Qt.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("draw__ellipse_board")

        self.cell_widget = CellWidget()

        self.pb_ball_size = Qt.QSpinBox()
        self.pb_ball_size.setRange(5, 1000)

        self.sl_ball_size = Qt.QSlider(Qt.Qt.Horizontal)
        self.sl_ball_size.setRange(
            self.pb_ball_size.minimum(), self.pb_ball_size.maximum()
        )

        self.sl_ball_size.valueChanged.connect(self._set_ball_size)
        self.pb_ball_size.valueChanged.connect(self._set_ball_size)

        self._set_ball_size(50)

        layout_command = Qt.QHBoxLayout()
        layout_command.addWidget(self.sl_ball_size)
        layout_command.addWidget(self.pb_ball_size)

        layout = Qt.QVBoxLayout()
        layout.addLayout(layout_command)
        layout.addWidget(self.cell_widget)

        self.setLayout(layout)

    def _set_ball_size(self, value):
        self.sl_ball_size.setValue(value)
        self.pb_ball_size.setValue(value)

        self.cell_widget.ball_size = value
        self.cell_widget.update()


if __name__ == "__main__":
    app = Qt.QApplication([])

    w = Window()
    w.resize(400, 400)
    w.show()

    app.exec()
