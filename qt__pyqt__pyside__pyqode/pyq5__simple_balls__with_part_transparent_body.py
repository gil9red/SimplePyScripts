#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from random import randint

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QTimer, Qt


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/1d6226ea5545e49b533e71c92d77856a7b2e171d/pygame__examples/simple_balls.py
# +
# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/00b9e4ec67e3413ffefa436a98381a75b99af6d3/qt__pyqt__pyside__pyqode/pyqt__frameless_window_with_part_transparent_body.py


class Ball:
    def __init__(self, x, y, r, v_x, v_y, color):
        self.x = x
        self.y = y
        self.r = r
        self.v_x = v_x
        self.v_y = v_y
        self.color = color

    def update(self):
        self.x += self.v_x
        self.y += self.v_y

    def draw(self, painter: QPainter):
        if isinstance(self.color, tuple):
            if len(self.color) == 4:
                r, g, b, a = self.color
                color = QColor(r, g, b, a)
            else:
                r, g, b = self.color
                color = QColor(r, g, b)
        else:
            color = self.color

        painter.save()
        painter.setPen(Qt.black)
        painter.setBrush(color)
        painter.drawEllipse(self.x, self.y, self.r, self.r)
        painter.restore()

    @property
    def center(self):
        return self.x, self.y

    @property
    def top(self):
        return self.y - self.r

    @property
    def bottom(self):
        return self.y + self.r

    @property
    def left(self):
        return self.x - self.r

    @property
    def right(self):
        return self.x + self.r


def get_random_vector() -> tuple[int, int]:
    pos = 0, 0
    # Если pos равен (0, 0), пересчитываем значения, т.к. шарик должен двигаться
    while pos == (0, 0):
        pos = randint(-3, 3), randint(-3, 3)

    return pos


def get_random_color() -> tuple[int, int, int]:
    return randint(0, 255), randint(0, 255), randint(0, 255)


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._old_pos = None
        self.frame_color = Qt.darkCyan

        self.balls: list[Ball] = []

        timeout = 1000 // 60

        # Таймер обновления движения и обработки столкновения шариков
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(timeout)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(QPushButton("Закрыть окно", clicked=self.close))

        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None

    def mouseMoveEvent(self, event):
        if not self._old_pos:
            return

        delta = event.pos() - self._old_pos
        self.move(self.pos() + delta)

    def tick(self):
        for ball in self.balls:
            ball.update()

            # Условия отскакивания шарика от левого и правого края
            if ball.left <= 0 or ball.right >= self.width():
                ball.v_x = -ball.v_x

            # Условия отскакивания шарика верхнего и нижнего края
            if ball.top <= 0 or ball.bottom >= self.height():
                ball.v_y = -ball.v_y

        # Вызов перерисовки
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(QColor(0, 0, 0, 1))
        painter.setPen(QPen(self.frame_color, 10))
        painter.drawRect(self.rect())

        for ball in self.balls:
            ball.draw(painter)

    def append_random_ball(self):
        x = self.width() // 2 + randint(-self.width() // 4, self.width() // 4)
        y = self.height() // 2 + randint(-self.height() // 4, self.height() // 4)
        r = randint(10, 20)
        v_x, v_y = get_random_vector()
        color = get_random_color()

        ball = Ball(x, y, r, v_x, v_y, color)
        self.balls.append(ball)


if __name__ == "__main__":
    app = QApplication([])

    WIDTH = 600  # ширина экрана
    HEIGHT = 600  # высота экрана
    BALL_NUMBER = 1000

    w = Widget()
    w.resize(WIDTH, HEIGHT)

    for i in range(BALL_NUMBER):
        w.append_random_ball()

    w.show()

    app.exec()
