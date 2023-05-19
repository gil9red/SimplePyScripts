#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from random import randint

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPaintEvent
from PyQt5.QtCore import QTimer

from full_black_screen_close_manual import MainWindow as BaseMainWindow
from pyq5__simple_balls__with_part_transparent_body import Ball, get_random_vector, get_random_color


class Animation:
    def __init__(self, owner: QWidget = None):
        self.owner = owner

    def set_owner(self, owner: QWidget):
        self.owner = owner

    def prepare(self):
        pass

    def tick(self):
        pass

    def draw(self, painter: QPainter):
        pass


class AnimationBalls(Animation):
    def __init__(self, owner: QWidget = None, number_balls: int = 50):
        super().__init__(owner)
        
        self.balls: list[Ball] = []
        self.number_balls = number_balls

    def prepare(self):
        for _ in range(self.number_balls):
            self.append_random_ball()

    def append_random_ball(self):
        x = self.owner.width() // 2 + randint(-self.owner.width() // 3, self.owner.width() // 3)
        y = self.owner.height() // 2 + randint(-self.owner.height() // 3, self.owner.height() // 3)
        v_x, v_y = get_random_vector()
        r, g, b = get_random_color()

        ball = Ball(
            x, y,
            r=randint(50, 70),
            v_x=v_x,
            v_y=v_y,
            color=(r, g, b, 15),
        )
        self.balls.append(ball)

    def tick(self):
        for ball in self.balls:
            ball.update()

            # Условия отскакивания шарика от левого и правого края
            if ball.left <= 0 or ball.right >= self.owner.width():
                ball.v_x = -ball.v_x

            # Условия отскакивания шарика верхнего и нижнего края
            if ball.top <= 0 or ball.bottom >= self.owner.height():
                ball.v_y = -ball.v_y

    def draw(self, painter: QPainter):
        for ball in self.balls:
            ball.draw(painter)


class MainWindow(BaseMainWindow):
    def __init__(self, animations: list[Animation] = None):
        super().__init__()

        self.animations: list[Animation] = animations

        # Таймер для обновления анимаций
        self.timer = QTimer()
        self.timer.setInterval(1000 // 20)
        self.timer.timeout.connect(self.tick)

    def tick(self):
        if not self.animations:
            return

        for animation in self.animations:
            animation.tick()

        self.update()

    def start_animations(self):
        if not self.animations:
            return

        for animation in self.animations:
            animation.set_owner(self)
            animation.prepare()

        self.timer.start()

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for animation in self.animations:
            animation.draw(painter)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow(
        animations=[
            AnimationBalls(),
        ]
    )
    mw.resize(600, 600)
    mw.showFullScreen()
    mw.start_animations()

    app.exec()
