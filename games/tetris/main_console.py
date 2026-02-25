#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time
from threading import Thread
from typing import Callable

from asciimatics.effects import Print
from asciimatics.renderers import FigletText, StaticRenderer
from asciimatics.event import Event, KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame
from asciimatics.exceptions import StopApplication, NextScene, ResizeScreenError

from src.core.board import Board
from src.core.piece import PieceO, PieceI, PieceS, PieceZ, PieceL, PieceJ, PieceT


# SOURCE: https://asciimatics.readthedocs.io/en/stable/io.html#colours
#         https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
PIECE_BY_COLOR = {
    PieceO(0, 0).get_color().name(): Screen.COLOUR_YELLOW,
    PieceI(0, 0).get_color().name(): Screen.COLOUR_CYAN,
    PieceS(0, 0).get_color().name(): Screen.COLOUR_GREEN,
    PieceZ(0, 0).get_color().name(): Screen.COLOUR_RED,
    PieceL(0, 0).get_color().name(): Screen.COLOUR_BLUE,
    PieceJ(0, 0).get_color().name(): Screen.COLOUR_MAGENTA,
    PieceT(0, 0).get_color().name(): Screen.COLOUR_WHITE,
}


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
        self.current_piece = self.board.current_piece
        self.is_fail = False

        self.next_scene = next_scene

        self.thread = Thread(target=self._run_timer, daemon=True)
        self.thread.start()

    def _run_timer(self) -> None:
        while self.board.do_step():
            time.sleep(0.3)

        self.is_fail = True

    def update(self, frame_no: int) -> None:
        super().update(frame_no)

        if self.is_fail:
            raise NextScene(self.next_scene)

        self.current_piece = self.board.current_piece

        self.screen.set_title(f"Tetris. Score: {self.board.score}")

        # Рисование заполненных ячеек
        for y, row in enumerate(self.board.matrix):
            for x, cell_color in enumerate(row):
                if not cell_color:
                    continue

                color = PIECE_BY_COLOR[cell_color.name()]
                # TODO: Рисовать квадратами, а не линиями
                self.screen.print_at(" ", x + 1, y + 1, bg=color)

        if self.current_piece:
            color = PIECE_BY_COLOR[self.current_piece.get_color().name()]
            for x, y in self.current_piece.get_points():
                # TODO: Рисовать квадратами, а не линиями
                self.screen.print_at(" ", x + 1, y + 1, bg=color)

    def process_event(self, event: Event):
        if isinstance(event, KeyboardEvent):
            key_code = event.key_code
            match key_code:
                case 81 | 113:  # Q | q
                    raise StopApplication("User requested exit")

                case 87 | 119 | Screen.KEY_UP:  # W | w
                    if self.current_piece:
                        self.current_piece.turn()

                case 65 | 97 | Screen.KEY_LEFT:  # A | a
                    if self.current_piece:
                        self.current_piece.move_left()

                case 68 | 100 | Screen.KEY_RIGHT:  # D | d
                    if self.current_piece:
                        self.current_piece.move_right()

                case 83 | 115 | Screen.KEY_DOWN:  # S | s
                    while self.current_piece and self.current_piece.move_down():
                        pass

        return event

    @property
    def frame_update_count(self) -> int:
        """
        Frame update rate required.
        """
        return 5


class NextPieceWidget(Frame):
    def __init__(
        self,
        board: Board,
        screen: Screen,
        y: int,
        x: int,
        height: int,
        width: int,
    ) -> None:
        self.y = y
        self.x = x
        self.height = height
        self.width = width

        super().__init__(
            screen,
            height=self.height,
            width=self.width,
            y=self.y,
            x=self.x,
            can_scroll=False,
            name="NextPieceWidget",
        )
        self.set_theme("monochrome")
        self.board = board
        self.next_piece = self.board.next_piece

    def update(self, frame_no: int) -> None:
        super().update(frame_no)

        self.next_piece = self.board.next_piece

        if self.next_piece:
            x_next = self.x + 3
            y_next = self.y
            color = PIECE_BY_COLOR[self.next_piece.get_color().name()]
            for x, y in self.next_piece.get_points_for_state(x=x_next, y=y_next):
                # TODO: Рисовать квадратами, а не линиями
                self.screen.print_at(" ", x + 1, y + 1, bg=color)

    def process_event(self, event: Event):
        return event

    @property
    def frame_update_count(self) -> int:
        return 5


class ScoreWidget(Frame):
    def __init__(
        self,
        board: Board,
        screen: Screen,
        y: int,
        x: int,
        height: int,
        width: int,
    ) -> None:
        self.y = y
        self.x = x
        self.height = height
        self.width = width

        super().__init__(
            screen,
            height=self.height,
            width=self.width,
            y=self.y,
            x=self.x,
            can_scroll=False,
            name="ScoreWidget",
        )
        self.set_theme("monochrome")
        self.board = board

    def update(self, frame_no: int) -> None:
        super().update(frame_no)

        self.screen.print_at(f"Score: {self.board.score}", self.x, self.y)

    def process_event(self, event: Event):
        return event

    @property
    def frame_update_count(self) -> int:
        return 5


def demo(screen: Screen, scene: Scene) -> None:
    board = Board()
    scenes = [
        Scene(
            [
                BoardWidget(
                    board,
                    screen,
                    y=0,
                    x=0,
                    width=board.COLS + 2,
                    height=board.ROWS + 2,
                    next_scene="LOSE",
                ),
                NextPieceWidget(
                    board, screen, y=0, x=board.COLS + 2, width=8, height=6
                ),
                ScoreWidget(board, screen, y=6, x=board.COLS + 2, width=8, height=2),
            ],
            duration=-1,
        ),
        Scene(
            [
                Print(
                    screen,
                    MyLateFigletText(
                        lambda: f"YOU LOSE!\nScore: {board.score}", font="standard"
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
