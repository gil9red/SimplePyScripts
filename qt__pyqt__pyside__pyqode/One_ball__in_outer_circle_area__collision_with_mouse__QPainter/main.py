#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/970882/201445
# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/d50de0f237d778f7d69ee75e328503f8c8344743/qt__pyqt__pyside__pyqode/QWebEngineView__one_ball__in_outer_circle_area__collision_with_mouse/index.html


from pathlib import Path
from timeit import default_timer

from PyQt5.Qt import QApplication, QWidget, QPainter, QTimer, Qt, QPoint, QPen


class Ball:
    r = 50  # Радиус шарика
    x = 0  # Координата по х центра шарика
    y = 0  # Координата по y центра шарика
    speed = 0  # Скорость движения
    dir_x = 0  # Компонент x вектора движения шарика
    dir_y = 0  # Компонент y вектора движения шарика
    damp = 10  # Скорость уменьшения скорости движения (сопротивление)
    collision = False  # Признак коллизии с внешним кругом
    speed_after_collision = 300  # Скорость движения шарика после столкновения

    # Функция, которая проверяет наличие коллизии шарика с внешним кругом
    def hit_outer_circle_check(self, outer_circle: int):
        dr = outer_circle - self.r  # Разница радиусов

        # По теореме пифагора проверяем выход за пределы круга (коллизию)
        if self.x * self.x + self.y * self.y > dr * dr:
            # Если коллизия уже была обсчитана, но шарик еще не вернулся в круг,
            # чтобы он не застревал больше не надо обсчитывать коллизии, поэтому выходим
            if self.collision:
                return

            # Устанавливаем для шарика признак коллизии
            self.collision = True

            # Далее идет код расчета нового вектора движения

            # Найдем вектор нормали. тут он берется приближенно,
            # в точке центра шарика в момент обсчета коллизии,
            # при том что шарик уже проскочил границу. по идее тут
            # необходимо посчитать точку соударения геометрически.
            max_value = max(abs(self.x), abs(self.y))
            nx = -self.x / max_value
            ny = -self.y / max_value

            # Найдем новый вектор движения по формуле
            # r = i−2(i⋅n)n , где
            # i - исходный вектор
            # n - нормаль
            # ⋅ знак скалярного произведения

            dot2 = self.dir_x * nx * 2 + self.dir_y * ny * 2
            self.dir_x = self.dir_x - dot2 * nx
            self.dir_y = self.dir_y - dot2 * ny

            # Нормализуем вектор движения
            max_value = max(abs(self.dir_x), abs(self.dir_y))
            self.dir_x /= max_value
            self.dir_y /= max_value

        else:
            # Сбрасываем признак коллизии когда шарик вернулся в круг.
            self.collision = False

    # Функция проверки коллизии шарика и мышки
    def hit_mouse_check(self, x, y):
        # Если есть коллизия с внешним кругом игнорируем мышку
        if self.collision:
            return

        # Разница координат мышки и шарика
        dx = self.x - x
        dy = self.y - y

        # Проверяем по теореме Пифагора столкновение с мышкой
        if dx * dx + dy * dy < self.r * self.r:
            # Задаем вектор движения и нормализуем его
            max_value = max(abs(dx), abs(dy))
            if not max_value:
                return

            self.dir_x = dx / max_value
            self.dir_y = dy / max_value

            # Задаем скорость
            self.speed = self.speed_after_collision

    # Тут осуществляется передвижение
    # dt - кол-во секунд с прошлого обсчета
    def do_move(self, dt):
        # К текущей координате прибавляем вектор скорости помноженный
        # на значение скорости помноженные на прошедшее время
        self.x += self.dir_x * self.speed * dt
        self.y += self.dir_y * self.speed * dt

        # Тормозим объект, так же на значение зависящее от времени
        self.speed = max(0, self.speed - self.damp * dt)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        title = Path(__file__).parent.name
        self.setWindowTitle(title)

        timeout = 1000 // 60

        # Таймер обновления движения и обработки столкновения шариков
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(timeout)

        # NOTE: Перерисовку помести в tick, но этот вариант с отдельным таймером тоже
        #       имеет право быть
        # # Таймер перерисовки окна
        # self.timer_render = QTimer()
        # self.timer_render.timeout.connect(self.update)
        # self.timer_render.start(timeout)

        self.outer_circle = 195
        self.ball = Ball()

        self.mouse_center_x = 0
        self.mouse_center_y = 0

        # Используется, чтобы в независимости от количества вызовов
        # tick скорость шарика была одинаковая
        self.t = 0

        self.setMouseTracking(True)

    def tick(self):
        # Считаем сколько времени прошло с прошлого обсчета
        dt = default_timer() - self.t

        self.ball.hit_mouse_check(self.mouse_center_x, self.mouse_center_y)
        self.ball.do_move(dt)
        self.ball.hit_outer_circle_check(self.outer_circle)

        self.t = default_timer()

        self.update()

    def mouseMoveEvent(self, event):
        self.mouse_center_x = event.pos().x() - (self.width() / 2)
        self.mouse_center_y = event.pos().y() - (self.height() / 2)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.setPen(QPen(Qt.red, 3))
        painter.setBrush(Qt.transparent)

        painter.translate(self.width() / 2, self.height() / 2)

        painter.drawEllipse(QPoint(0, 0), self.outer_circle, self.outer_circle)
        painter.drawEllipse(QPoint(self.ball.x, self.ball.y), self.ball.r, self.ball.r)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
