#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
from random import randint, choice

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPaintEvent
from PyQt5.QtCore import QTimer

from full_black_screen_close_manual import MainWindow as BaseMainWindow
from pyq5__simple_balls__with_part_transparent_body import (
    Ball as BaseBall,
    get_random_vector,
    get_random_color,
)


class Animation:
    def __init__(self, owner: QWidget = None) -> None:
        self.owner = owner

    def set_owner(self, owner: QWidget) -> None:
        self.owner = owner

    def prepare(self) -> None:
        pass

    def tick(self) -> None:
        pass

    def draw(self, painter: QPainter) -> None:
        pass


class DirectionEnum(enum.IntEnum):
    UP = 1
    DOWN = -1


class Ball(BaseBall):
    def __init__(self, x, y, r, v_x, v_y, color) -> None:
        super().__init__(x, y, r, v_x, v_y, color)

        self.animation_alpha_direction = choice(list(DirectionEnum))


class AnimationBalls(Animation):
    def __init__(
        self,
        owner: QWidget = None,
        number_balls: int = 50,
        min_ball_alpha_color: int = 35,  # Минимальное значение может быть 0
        max_ball_alpha_color: int = 160,  # Максимальное значение может быть 255
        animation_ball_alpha_color: bool = True,
    ) -> None:
        super().__init__(owner)

        self.balls: list[Ball] = []
        self.number_balls = number_balls
        self.min_ball_alpha_color = min_ball_alpha_color
        self.max_ball_alpha_color = max_ball_alpha_color
        self.animation_ball_alpha_color = animation_ball_alpha_color

    def prepare(self) -> None:
        for _ in range(self.number_balls):
            self.append_random_ball()

    def append_random_ball(self) -> None:
        x = self.owner.width() // 2 + randint(
            -self.owner.width() // 3, self.owner.width() // 3
        )
        y = self.owner.height() // 2 + randint(
            -self.owner.height() // 3, self.owner.height() // 3
        )
        v_x, v_y = get_random_vector()
        r, g, b = get_random_color()
        a = randint(self.min_ball_alpha_color, self.max_ball_alpha_color)

        ball = Ball(
            x,
            y,
            r=randint(50, 70),
            v_x=v_x,
            v_y=v_y,
            color=(r, g, b, a),
        )
        self.balls.append(ball)

    def tick(self) -> None:
        for ball in self.balls:
            ball.update()

            # Условия отскакивания шарика от левого и правого края
            if ball.left <= 0 or ball.right >= self.owner.width():
                ball.v_x = -ball.v_x

            # Условия отскакивания шарика верхнего и нижнего края
            if ball.top <= 0 or ball.bottom >= self.owner.height():
                ball.v_y = -ball.v_y

            if self.animation_ball_alpha_color:
                alpha = ball.color[3] + ball.animation_alpha_direction

                if alpha >= self.max_ball_alpha_color:
                    ball.animation_alpha_direction = DirectionEnum.DOWN

                if alpha <= self.min_ball_alpha_color:
                    ball.animation_alpha_direction = DirectionEnum.UP

                ball.color = ball.color[:3] + (alpha,)

    def draw(self, painter: QPainter) -> None:
        for ball in self.balls:
            ball.draw(painter)


class MainWindow(BaseMainWindow):
    def __init__(self, animations: list[Animation] = None) -> None:
        super().__init__()

        self.animations: list[Animation] = animations

        # Таймер для обновления анимаций
        self.timer = QTimer()
        self.timer.setInterval(1000 // 20)
        self.timer.timeout.connect(self.tick)

    def tick(self) -> None:
        if not self.animations:
            return

        for animation in self.animations:
            animation.tick()

        self.update()

    def start_animations(self) -> None:
        if not self.animations:
            return

        for animation in self.animations:
            animation.set_owner(self)
            animation.prepare()

        self.timer.start()

    def paintEvent(self, event: QPaintEvent) -> None:
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
