#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time
from threading import Thread
from typing import Callable

from asciimatics.effects import Print
from asciimatics.renderers import FigletText, StaticRenderer
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, Layout, Text, Button
from asciimatics.exceptions import NextScene, ResizeScreenError

from board import Board, StepResultEnum, get_random_seed


class MyLateFigletText(StaticRenderer):
    def __init__(self, rendered_text_func: Callable[[], str], **kwargs) -> None:
        super().__init__()

        self.rendered_text_func = rendered_text_func
        self.kwargs = kwargs

    @property
    def rendered_text(self):
        renderer = FigletText(
            text=self.rendered_text_func(),
            **self.kwargs,
        )
        return renderer.rendered_text


class BoardWidget(Frame):
    def __init__(
        self,
        board: Board,
        screen: Screen,
        y: int,
        x: int,
        height: int,
        width: int,
        next_scene: str,
    ) -> None:
        self.y = y
        self.x = x
        self.height = height
        self.width = width

        super().__init__(
            screen,
            height=self.height,
            width=self.width,
            x=self.x,
            y=self.y,
            can_scroll=False,
            name="BoardWidget",
        )
        self.set_theme("monochrome")

        self.board = board
        self.is_fail = False
        self.timer_secs: float = 0.5

        self.next_scene = next_scene

        self.thread = Thread(target=self._run_timer, daemon=True)

    def start(self, timer_ms: int, seed: str) -> None:
        self.is_fail = False
        self.timer_secs = timer_ms / 1000

        self.board.rows = self.height - 2
        self.board.cols = self.width - 2
        self.board.generate(seed)

        # TODO: RuntimeError: threads can only be started once
        self.thread.start()

    def _run_timer(self) -> None:
        while self.board.do_step() == StepResultEnum.OK:
            time.sleep(self.timer_secs)

        self.is_fail = True

    def update(self, frame_no: int):
        super().update(frame_no)

        if self.is_fail:
            raise NextScene(self.next_scene)

        self.screen.set_title(
            f"Life. "
            f"Board: {self.board.rows}x{self.board.cols}. "
            f"Seed: {self.board.seed}. "
            f"Generation: {self.board.generation_number}. "
            f"Living cells: {self.board.count_living_cells}"
        )

        # Рисование заполненных ячеек
        for y, row in enumerate(self.board.matrix):
            for x, cell_color in enumerate(row):
                if not cell_color:
                    continue

                self.screen.print_at(
                    " ", self.x + x + 1, self.y + y + 1, bg=Screen.COLOUR_WHITE
                )

    @property
    def frame_update_count(self) -> int:
        """
        Frame update rate required.
        """
        return 5


class MenuWidget(Frame):
    def __init__(
            self,
            screen: Screen,
            y: int, x: int, height: int, width: int,
    ) -> None:
        self.y = y
        self.x = x
        self.height = height
        self.width = width

        super().__init__(
            screen,
            height=self.height,
            width=self.width,
            x=self.x,
            y=self.y,
            hover_focus=True,
            can_scroll=False,
            name="MenuWidget",
            reduce_cpu=True,
        )
        self.set_theme("monochrome")

        self.on_click_start: Callable[[int, str], None] = None

        # TODO: validator не работает
        self.le_timer = Text("Timer (ms):", "timer_ms", validator=r"\d+")
        self.le_timer.value = "50"

        self.le_seed = Text("Seed:", "seed")
        self.le_seed.value = get_random_seed()

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        layout.add_widget(self.le_timer)
        layout.add_widget(self.le_seed)
        layout.add_widget(Button("Start", self._start))

        self.fix()

    def get_timer_ms(self) -> int:
        return int(self.le_timer.value)

    def get_seed(self) -> str:
        return self.le_seed.value

    def _start(self) -> None:
        # TODO: validator не работает. Не помогает save и validate
        self.save(validate=True)

        if callable(self.on_click_start):
            self.on_click_start(
                self.get_timer_ms(),
                self.get_seed(),
            )


def demo(screen: Screen, scene: Scene) -> None:
    menu_widget = MenuWidget(
        screen,
        y=0, x=0,
        width=screen.width, height=5,
    )

    board = Board()
    board_widget = BoardWidget(
        board,
        screen,
        y=menu_widget.height,
        x=0,
        width=screen.width,
        height=screen.height - menu_widget.height,
        next_scene="LOSE",
    )

    menu_widget.on_click_start = board_widget.start

    scenes = [
        Scene(
            [menu_widget, board_widget],
            duration=-1,
            name="GAME",
        ),
        Scene(
            [
                Print(
                    screen,
                    MyLateFigletText(
                        lambda: f"YOU LOSE!\nResult: {board.last_step_result.name}",
                        font="standard",
                    ),
                    x=0,
                    y=screen.height // 3 - 3,
                ),
            ],
            duration=-1,
            name="LOSE",
        ),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene)


last_scene = None
while True:
    try:
        Screen.wrapper(
            demo,
            # TODO:
            # catch_interrupt=True,
            arguments=[last_scene],
        )
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
