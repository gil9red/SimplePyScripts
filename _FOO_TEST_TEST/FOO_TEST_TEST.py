#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import traceback
from random import randint
from timeit import default_timer

from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QMessageBox,
    QMainWindow,
)
from PyQt6.QtCore import QRectF, QLineF, Qt, QTimer


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}\n"
    text += "".join(traceback.format_tb(tb))
    print(text)

    if QApplication.instance():
        msg_box = QMessageBox(
            QMessageBox.Critical,
            "Error",
            f"Error: {ex}",
            parent=None,
        )
        msg_box.setDetailedText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()


sys.excepthook = log_uncaught_exceptions


# TODO: Пусть будет 13 x 3
board = """\
  x x x x x  
xxx  xxx  xxx
xxx  x x  xxx
""".rstrip()
# TODO:
brick_width: int = 40
brick_height: int = 20

app = QApplication([])

scene_width, scene_height = 600, 300
scene_rect = QRectF(0, 0, scene_width, scene_height)

scene = QGraphicsScene()
scene.setSceneRect(scene_rect)

# TODO: У линий есть проблема с координатами как у QRectF?
scene_top_line_item = scene.addLine(QLineF(scene_rect.topLeft(), scene_rect.topRight()))
scene_left_line_item = scene.addLine(
    QLineF(scene_rect.topLeft(), scene_rect.bottomLeft())
)
scene_bottom_line_item = scene.addLine(
    QLineF(scene_rect.bottomRight(), scene_rect.bottomLeft())
)
scene_right_line_item = scene.addLine(
    QLineF(scene_rect.topRight(), scene_rect.bottomRight())
)

print(
    "scene_top_line_item",
    scene_top_line_item.sceneBoundingRect(),
    scene_top_line_item.sceneBoundingRect().bottom(),
)
print(
    "scene_left_line_item",
    scene_left_line_item.sceneBoundingRect(),
    scene_left_line_item.sceneBoundingRect().right(),
)
print(
    "scene_bottom_line_item",
    scene_bottom_line_item.sceneBoundingRect(),
    scene_bottom_line_item.sceneBoundingRect().top(),
)
print(
    "scene_right_line_item",
    scene_right_line_item.sceneBoundingRect(),
    scene_right_line_item.sceneBoundingRect().left(),
)

bricks: list[QGraphicsRectItem] = []
top: int = 0
for line in board.splitlines():
    print(repr(line))
    left: int = 0
    for x in line:
        if x == "x":
            ball_item = scene.addRect(
                QRectF(0, 0, brick_width, brick_height),
                brush=Qt.GlobalColor.red,
            )
            ball_item.setPos(left, top)
            bricks.append(ball_item)
        left += brick_width

    top += brick_height

ball_radius: int = 40

platform_width: int = 100
platform_height: int = 20

# TODO:
platform_item = scene.addRect(
    QRectF(
        0,
        0,
        platform_width,
        platform_height,
    ),
    brush=Qt.GlobalColor.red,
)
platform_item.setPos(
    (scene.width() / 2) - (platform_width / 2), scene.height() - platform_height
)
platform_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

ball_item = scene.addEllipse(
    QRectF(
        0,
        0,
        ball_radius,
        ball_radius,
    ),
    brush=Qt.GlobalColor.green,
)
ball_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

ball_item.setPos(
    platform_item.sceneBoundingRect().center().x()
    - (ball_item.sceneBoundingRect().width() / 2),
    platform_item.sceneBoundingRect().top() - ball_item.sceneBoundingRect().height(),
)


class Ball:
    def __init__(self, ball_item: QGraphicsEllipseItem, v_x, v_y):
        # def __init__(self, x, y, r, v_x, v_y, color):
        # TODO:
        self.x = ball_item.x()
        self.y = ball_item.y()
        self.r = ball_item.sceneBoundingRect().width()

        self.ball_item = ball_item
        self.v_x = v_x
        self.v_y = v_y

        self.is_collision: bool = False
        # self.color = color

    def update(self):
        self.x += self.v_x
        self.y += self.v_y

        self.ball_item.setPos(self.x, self.y)

    # def draw(self):
    # # def draw(self, screen):
    #     self.ball_item.setPos(self.center)
    #     # pygame.draw.circle(screen, self.color, self.center, self.r)
    #     #
    #     # # Нарисуем поверх первого, прозрачный второй с границей (параметр width)
    #     # pygame.draw.circle(screen, (0, 0, 0), self.center, self.r, 1)

    # @property
    # def center(self):
    #     return self.x, self.y
    #
    # @property
    # def top(self):
    #     return self.y - self.r
    #
    # @property
    # def bottom(self):
    #     return self.y + self.r
    #
    # @property
    # def left(self):
    #     return self.x - self.r
    #
    # @property
    # def right(self):
    #     return self.x + self.r


# class Ball:
#     r = 50  # Радиус шарика
#     x = 0  # Координата по х центра шарика
#     y = 0  # Координата по y центра шарика
#     speed = 0  # Скорость движения
#     dir_x = 0  # Компонент x вектора движения шарика
#     dir_y = 0  # Компонент y вектора движения шарика
#     # TODO: Не нужно
#     damp = 10  # Скорость уменьшения скорости движения (сопротивление)
#     collision = False  # Признак коллизии с внешним кругом
#     # TODO: Не нужно
#     speed_after_collision = 300  # Скорость движения шарика после столкновения
#
#     # # Функция, которая проверяет наличие коллизии шарика с внешним кругом
#     # def hit_outer_circle_check(self, outer_circle: int):
#     #     dr = outer_circle - self.r  # Разница радиусов
#     #
#     #     # По теореме пифагора проверяем выход за пределы круга (коллизию)
#     #     if self.x * self.x + self.y * self.y > dr * dr:
#     #         # Если коллизия уже была обсчитана, но шарик еще не вернулся в круг,
#     #         # чтобы он не застревал больше не надо обсчитывать коллизии, поэтому выходим
#     #         if self.collision:
#     #             return
#     #
#     #         # Устанавливаем для шарика признак коллизии
#     #         self.collision = True
#     #
#     #         # Далее идет код расчета нового вектора движения
#     #
#     #         # Найдем вектор нормали. тут он берется приближенно,
#     #         # в точке центра шарика в момент обсчета коллизии,
#     #         # при том что шарик уже проскочил границу. по идее тут
#     #         # необходимо посчитать точку соударения геометрически.
#     #         max_value = max(abs(self.x), abs(self.y))
#     #         nx = -self.x / max_value
#     #         ny = -self.y / max_value
#     #
#     #         # Найдем новый вектор движения по формуле
#     #         # r = i−2(i⋅n)n , где
#     #         # i - исходный вектор
#     #         # n - нормаль
#     #         # ⋅ знак скалярного произведения
#     #
#     #         dot2 = self.dir_x * nx * 2 + self.dir_y * ny * 2
#     #         self.dir_x = self.dir_x - dot2 * nx
#     #         self.dir_y = self.dir_y - dot2 * ny
#     #
#     #         # Нормализуем вектор движения
#     #         max_value = max(abs(self.dir_x), abs(self.dir_y))
#     #         self.dir_x /= max_value
#     #         self.dir_y /= max_value
#     #
#     #     else:
#     #         # Сбрасываем признак коллизии когда шарик вернулся в круг.
#     #         self.collision = False
#     #
#     # # Функция проверки коллизии шарика и мышки
#     # def hit_mouse_check(self, x, y):
#     #     # Если есть коллизия с внешним кругом игнорируем мышку
#     #     if self.collision:
#     #         return
#     #
#     #     # Разница координат мышки и шарика
#     #     dx = self.x - x
#     #     dy = self.y - y
#     #
#     #     # Проверяем по теореме Пифагора столкновение с мышкой
#     #     if dx * dx + dy * dy < self.r * self.r:
#     #         # Задаем вектор движения и нормализуем его
#     #         max_value = max(abs(dx), abs(dy))
#     #         if not max_value:
#     #             return
#     #
#     #         self.dir_x = dx / max_value
#     #         self.dir_y = dy / max_value
#     #
#     #         # Задаем скорость
#     #         self.speed = self.speed_after_collision
#
#     # Тут осуществляется передвижение
#     # dt - кол-во секунд с прошлого обсчета
#     def do_move(self, dt):
#         # К текущей координате прибавляем вектор скорости помноженный
#         # на значение скорости помноженные на прошедшее время
#         self.x += self.dir_x * self.speed * dt
#         self.y += self.dir_y * self.speed * dt
#
#         # Тормозим объект, так же на значение зависящее от времени
#         self.speed = max(0, self.speed - self.damp * dt)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TODO")

        self.view = QGraphicsView()
        self.view.setScene(scene)

        scene.changed.connect(self.on_scene_changed)

        timeout = 1000 // 60

        # Используется, чтобы в независимости от количества вызовов
        # tick скорость шарика была одинаковая
        self.t = 0

        # Таймер обновления движения и обработки столкновения шариков
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        # TODO:
        # self.timer.start(timeout)

        # TODO: Вектор вниз не нужно генерировать
        def get_random_vector() -> tuple[int, int]:
            pos = 0, 0
            # Если pos равен (0, 0), пересчитываем значения, т.к. шарик должен двигаться
            while pos == (0, 0):
                pos = randint(-3, 3), randint(-3, 3)

            return pos

        v_x, v_y = get_random_vector()
        self.ball = Ball(ball_item=ball_item, v_x=v_x, v_y=v_y)
        # self.ball.dir_x
        # self.ball.r = ball_item.sceneBoundingRect().width() # TODO:
        # self.ball.x = ball_item.sceneBoundingRect().center().x() # TODO: просто ball_item.x()?
        # self.ball.y = ball_item.sceneBoundingRect().center().y()

        self.setCentralWidget(self.view)

    # TODO:
    def tick(self):
        # TODO: Использовать
        # Считаем сколько времени прошло с прошлого обсчета
        dt = default_timer() - self.t

        # self.ball.hit_mouse_check(self.mouse_center_x, self.mouse_center_y)
        # self.ball.do_move(dt)
        # self.ball.hit_outer_circle_check(self.outer_circle)

        ball = self.ball  # TODO:
        # ball.draw()
        ball.update()

        # TODO: определять глубину проникновения шарика за границы и выталкивать его перед сменой вектора движения

        # # Условия отскакивания шарика от левого и правого края
        # if ball.left <= 0 or ball.right >= self.width:
        #     ball.v_x = -ball.v_x
        #
        # # Условия отскакивания шарика верхнего и нижнего края
        # if ball.top <= 0 or ball.bottom >= self.height:
        #     ball.v_y = -ball.v_y

        self.t = default_timer()
        #
        # self.update()

    def on_scene_changed(self, region: list[QRectF]):
        print("on_scene_changed", region)

        # if self.ball.is_collision:
        #     return

        # TODO: технически, ball_item может быть много

        # TODO: Проверка выхода за сцену ball_item
        colliding_items = ball_item.collidingItems()
        print(colliding_items)

        # for item in colliding_items:
        #     color = Qt.GlobalColor.darkMagenta if item.collidesWithItem(ball_item) else Qt.GlobalColor.red
        #
        #     if isinstance(item, QGraphicsRectItem):
        #         item.setBrush(color)
        #     elif isinstance(item, QGraphicsLineItem):
        #         item.setPen(color)

        collisions: list[str] = []
        for brick in bricks:
            brick.setBrush(
                Qt.GlobalColor.darkMagenta
                if brick.collidesWithItem(ball_item)
                else Qt.GlobalColor.red
            )
            if brick in colliding_items:
                # if brick.collidesWithItem(ball_item):  # TODO:
                collisions.append("brick")

        # NOTE: Фиксация по Y
        platform_item.setY(scene.sceneRect().bottom() - platform_height)

        if (
            platform_item.sceneBoundingRect().left()
            <= scene_left_line_item.sceneBoundingRect().right()
        ):
            platform_item.setX(scene_left_line_item.sceneBoundingRect().right())
        elif (
            platform_item.sceneBoundingRect().right()
            >= scene_right_line_item.sceneBoundingRect().left()
        ):
            # TODO: Немного не доходит до границ
            platform_item.setX(
                scene_right_line_item.sceneBoundingRect().left()
                - platform_item.sceneBoundingRect().width()
            )

        # if platform_item.collidesWithItem(ball_item):  # TODO:
        if platform_item in colliding_items:
            platform_item.setBrush(Qt.GlobalColor.darkMagenta)
            collisions.append("platform")
        else:
            platform_item.setBrush(Qt.GlobalColor.red)

        # if scene_top_line_item.collidesWithItem(ball_item):  # TODO:
        if scene_top_line_item in colliding_items:
            collisions.append("top")
            scene_top_line_item.setPen(Qt.GlobalColor.red)
        else:
            scene_top_line_item.setPen(Qt.GlobalColor.black)

        # if scene_right_line_item.collidesWithItem(ball_item):  # TODO:
        if scene_right_line_item in colliding_items:
            collisions.append("right")
            scene_right_line_item.setPen(Qt.GlobalColor.red)
        else:
            scene_right_line_item.setPen(Qt.GlobalColor.black)

        # if scene_bottom_line_item.collidesWithItem(ball_item):  # TODO:
        if scene_bottom_line_item in colliding_items:
            collisions.append("bottom")
            scene_bottom_line_item.setPen(Qt.GlobalColor.red)
        else:
            scene_bottom_line_item.setPen(Qt.GlobalColor.black)

        # if scene_left_line_item.collidesWithItem(ball_item):  # TODO:
        if scene_left_line_item in colliding_items:
            collisions.append("left")
            scene_left_line_item.setPen(Qt.GlobalColor.red)
        else:
            scene_left_line_item.setPen(Qt.GlobalColor.black)

        self.setWindowTitle(
            f"collidingItems: {len(colliding_items)}. Collisions: {', '.join(collisions)}"
        )

        # Условия отскакивания шарика от левого и правого края
        ball = self.ball  # TODO:
        # ball.is_collision = bool(collisions)

        if "left" in collisions or "right" in collisions:
            ball.v_x = -ball.v_x
            ball.is_collision = True
        else:
            ball.is_collision = False

        # Условия отскакивания шарика верхнего и нижнего края
        if "top" in collisions or "bottom" in collisions:
            ball.v_y = -ball.v_y
            ball.is_collision = True
        else:
            ball.is_collision = False


mw = MainWindow()

# TODO:
# n = 3
# view.scale(1.0 / n, 1.0 / n)

mw.resize(scene_width + 20, scene_height + 20)
mw.show()

app.exec()


quit()

from datetime import date, timedelta

start = date(year=1992, month=8, day=18)
year = 1
while True:
    print(year, start)
    start += timedelta(days=365)
    year += 1
    if start.year > 2025:
        break

# print((date.today() - ).days / 366)

quit()

from pathlib import Path

from typing import Any, Generator, Sized


def chunks(l: Sized, n: int) -> Generator[Any, None, None]:
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


p = Path("C:/Users/ipetrash/Downloads/0000_0039_Trnv_P_20250201_01_CIB0983543.ebc")
data = p.read_bytes()
for line in chunks(data, 170):
    print(line.hex().upper())

quit()

import copy2clipboard__via_pyperclip as copy2clipboard

while n := input():
    value = n.title()
    copy2clipboard.to(value)
    print(value + "\n")


quit()

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDockWidget,
    QMainWindow,
    QTextEdit,
    QPushButton,
)

import sys
import traceback

from PyQt5.QtWidgets import QApplication, QTextEdit, QMessageBox


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


app = QApplication([])

dock_widget_2 = QDockWidget("Right2")
pb = QPushButton("!!!", clicked=dock_widget_2.setFloating)
pb.setCheckable(True)
dock_widget_2.setTitleBarWidget(pb)

dock_widget_left = QDockWidget("Left")
# TODO: Добавить кнопку PIN, которая вытаскивает доквиджет, отвязывает от родителя, делает поверх всех окон
#       Показывать кнопку возврата обратно
dock_widget_left.topLevelChanged.connect(
    lambda flag: (
        dock_widget_left.setWindowFlag(Qt.WindowStaysOnTopHint, flag),
        dock_widget_left.setParent(None) if flag else None,
        dock_widget_left.show(),
    )
)
# dock_widget_left.setWindowFlags(Qt.WindowType.Window)
# dock_widget_left.show()

mw = QMainWindow()
mw.setCentralWidget(QTextEdit())
mw.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, QDockWidget("Right"))
mw.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_widget_2)
mw.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_widget_left)
mw.show()

app.exec()


quit()

from dataclasses import dataclass, field
from datetime import datetime, timedelta, date, timezone


def add_to_month(d: date, inc: bool = True, number: int = 1) -> date:
    d = d.replace(day=1)

    year = d.year
    month = d.month

    for _ in range(number):
        month += 1 if inc else -1
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1

        d = date(year=year, month=month, day=1)

    return d


"""
Date: 06 мая 2024 г. 21:11:42 | Release version 3.2.40.10 (release based on revision 324264)
Date: 03 июля 2024 г. 19:11:35 | Release version 3.2.41.10 (release based on revision 327113)
Date: 04 сентября 2024 г. 15:08:49 | Release version 3.2.42.10 (release based on revision 330920)
Date: 05 ноября 2024 г. 19:40:28 | Release version 3.2.43.10 (release based on revision 335027)

26, 11.01.2022, 14.03.2022, 15.11.2022 +8,

27, 03.03.2022, 27.05.2022, 09.12.2022 +7, +1
28, 05.05.2022, 15.07.2022, 10.02.2023 +7, +2
29, 04.07.2022, 15.09.2022, 24.05.2023 +8, +3

30, 01.09.2022, 15.11.2022, 05.06.2023 +7, +1
31, 01.11.2023, 19.01.2023, 01.08.2023 +7, +2
32, 09.01.2023, 14.03.2023, 07.11.2023 +8, +3

33, 02.03.2023, 18.05.2023, 04.12.2023 +7, +1
34, 04.05.2023, 21.07.2023, 01.02.2024 +7, +2
35, 05.07.2023, 15.09.2023, 03.05.2024 +8, +3

36, 04.09.2023, 21.11.2023, 07.06.2024 +7, +1
37, 02.11.2023, 23.01.2024, 05.08.2024 +7, +2
38, 11.01.2024, 15.03.2024, 28.11.2024 +8, +3
"""


INIT_RELEASE_VERSION: int = 31
INIT_RELEASE_DATE: date = date(year=2022, month=11, day=1)


@dataclass
class Release:
    version: int
    date: date
    free_commit_date: date = field(init=False)
    testing_finish_date: date = field(init=False)
    support_end_date: date = field(init=False)

    def __post_init__(self):
        self.free_commit_date = add_to_month(self.date, number=1) - timedelta(days=1)
        self.testing_finish_date = add_to_month(self.date, number=2)
        self.support_end_date = add_to_month(
            self.testing_finish_date,
            # NOTE: Месяца 3 и 9, похоже, связаны с IPS mandates
            number=8 if self.testing_finish_date.month in (3, 9) else 7,
        )

    @classmethod
    def get_by(cls, d: date = None, version: int = None) -> "Release":
        if d is None and version is None:
            # TODO: Нормальное исключение
            raise Exception()

        if d is not None:
            _is_found = lambda r: r.date <= d < r.testing_finish_date
        else:
            _is_found = lambda r: r.version == version

        if d is not None:
            _is_need_next = lambda r: d > r.date
        else:
            _is_need_next = lambda r: version > r.version

        release = Release(
            version=INIT_RELEASE_VERSION,
            date=INIT_RELEASE_DATE,
        )

        while True:
            if _is_found(release):
                return release

            release = (
                release.get_next_release()
                if _is_need_next(release)
                else release.get_prev_release()
            )

    @classmethod
    def get_by_date(cls, d: date) -> "Release":
        return cls.get_by(d=d)

    @classmethod
    def get_by_version(cls, version: int) -> "Release":
        return cls.get_by(version=version)

    @classmethod
    def get_last_release(cls) -> "Release":
        return cls.get_by_date(date.today())

    def get_next_release(self) -> "Release":
        return Release(
            version=self.version + 1,
            date=add_to_month(self.date, number=2),
        )

    def get_prev_release(self) -> "Release":
        return Release(
            version=self.version - 1,
            date=add_to_month(self.date, inc=False, number=2),
        )

    def is_last_release(self) -> bool:
        return self == self.get_last_release()


last_release: Release = Release.get_last_release()
print("last_release:", last_release)
print("trunk:", last_release.get_next_release())
print()

releases: list[Release] = [
    Release.get_by_version(version)
    for version in range(last_release.version - 6, last_release.version + 6 + 1)
]
for release in releases:
    print(release, release.is_last_release())


# for _ in range(15):
#     release = releases[-1]
#     releases.append(release.get_next_release())


# TODO: В тесты
# release = releases[-1]
# releases_v2 = [release]
# for _ in range(15):
#     release = release.get_prev_release()
#     releases_v2.append(release)
# print(releases_v2 == releases)
#
# for r1, r2 in zip(releases, releases_v2[::-1]):
#     print(r1 == r2)
#     print(f"{r1}\n{r2}")
#     print()

# for r in releases:
#     print(r)


# d = date.today().replace(day=1)
# print(d)
# print()
#
# for _ in range(20):
#     d = change_month(d)
#     print(d)


print("\n" + "-" * 100 + "\n")


def get_items(
    start_date: date,
    end_date: date,
    delta: timedelta,
) -> list[tuple[date, date]]:
    items = []

    dt = end_date
    while True:
        if dt <= start_date:
            break

        dt1 = dt
        dt -= delta

        if dt < start_date:
            dt = start_date

        items.append((dt, dt1))

    return items


def to_ms(d: date) -> int:
    utc_timestamp = datetime.combine(
        d, datetime.min.time(), tzinfo=timezone.utc
    ).timestamp()
    return int(utc_timestamp * 1000)


d = datetime.utcnow().date()
print(d)
# 2025-01-10

for d1, d2 in get_items(
    start_date=d - timedelta(weeks=6),
    end_date=d + timedelta(days=1),
    delta=timedelta(weeks=1),
):
    print(f"{d1} - {d2}. {to_ms(d1)}+{to_ms(d2)}")
"""
2025-01-04 - 2025-01-11. 1735948800000+1736553600000
2024-12-28 - 2025-01-04. 1735344000000+1735948800000
2024-12-21 - 2024-12-28. 1734739200000+1735344000000
2024-12-14 - 2024-12-21. 1734134400000+1734739200000
2024-12-07 - 2024-12-14. 1733529600000+1734134400000
2024-11-30 - 2024-12-07. 1732924800000+1733529600000
2024-11-29 - 2024-11-30. 1732838400000+1732924800000
"""
