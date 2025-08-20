#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsLineItem,
)
from PyQt6.QtCore import QRectF, QLineF, Qt


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
scene_top_line_item = scene.addLine(
    QLineF(scene_rect.topLeft(), scene_rect.topRight())
)  # TODO: ?
scene_left_line_item = scene.addLine(
    QLineF(scene_rect.topLeft(), scene_rect.bottomLeft())
)  # TODO: ?
scene_bottom_line_item = scene.addLine(
    QLineF(scene_rect.bottomRight(), scene_rect.bottomLeft())
)  # TODO: ?
scene_right_line_item = scene.addLine(
    QLineF(scene_rect.topRight(), scene_rect.bottomRight())
)  # TODO: ?
# scene_rect_item = scene.addRect(scene_rect)  # TODO: ?
scene.setSceneRect(scene_rect)

bricks: list[QGraphicsRectItem] = []
top: int = 0
for line in board.splitlines():
    print(repr(line))
    left: int = 0
    for x in line:
        if x == "x":
            bricks.append(
                scene.addRect(
                    QRectF(left, top, brick_width, brick_height),
                    brush=Qt.GlobalColor.red,
                )
            )
        left += brick_width

    top += brick_height

ball_radius: int = 40

platform_width: int = 100
platform_height: int = 20

# TODO:
platform_item = scene.addRect(
    QRectF(
        (scene.width() / 2) - (platform_width / 2),
        scene.height() - platform_height,
        platform_width,
        platform_height,
    ),
    brush=Qt.GlobalColor.red,
)

ball_item = scene.addEllipse(
    QRectF(
        scene.width() / 2 - (ball_radius / 2),
        scene.height() - ball_radius - platform_height,
        ball_radius,
        ball_radius,
    ),
    brush=Qt.GlobalColor.green,
)
ball_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)


def on_scene_changed(region: list[QRectF]):
    print("on_scene_changed", region)

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
        if brick.collidesWithItem(ball_item):  # TODO:
            collisions.append("brick")

    if platform_item.collidesWithItem(ball_item):  # TODO:
        collisions.append("platform")

    if scene_top_line_item.collidesWithItem(ball_item):  # TODO:
        collisions.append("top")

    if scene_right_line_item.collidesWithItem(ball_item):  # TODO:
        collisions.append("right")

    if scene_bottom_line_item.collidesWithItem(ball_item):  # TODO:
        collisions.append("bottom")

    if scene_left_line_item.collidesWithItem(ball_item):  # TODO:
        collisions.append("left")

    view.setWindowTitle(
        f"collidingItems: {len(colliding_items)}. Collisions: {', '.join(collisions)}"
    )


scene.changed.connect(on_scene_changed)

view = QGraphicsView()
view.setWindowTitle("TODO")
view.setScene(scene)

# n = 3
# view.scale(1.0 / n, 1.0 / n)

view.resize(scene_width + 20, scene_height + 20)

view.show()

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
