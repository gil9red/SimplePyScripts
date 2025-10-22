#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass
from random import randint

import time
import os

# pip install pynput-1.8.1
from pynput import keyboard


BOARD_TEMPLATE = """
##############################
#G                           #
########  #######  #######   #
#  GG  #                     #
#  GG  #  # G G G G G G  #   #
#  GG  #  ################   #
#  GG  #                     #
#      #  ######  ### ####   #
#         #GG  #  # # #GG#   #
#         #GG     #      # @ #
##############################
""".strip()


def clear():
    os.system("clear" if os.name == "posix" else "cls")


@dataclass
class GameObject:
    pos_x: int = 0
    pos_y: int = 0

    icon: str = " "


@dataclass
class Wall(GameObject):
    icon: str = "#"


@dataclass
class Gold(GameObject):
    value: int = 0
    icon: str = "G"


@dataclass
class Hero(GameObject):
    gold: int = 0
    icon: str = "@"


class Game:
    def __init__(self):
        self.hero: Hero = Hero()
        self.board: list[list[GameObject]] = []
        self.is_active: bool = False

        self.listener = keyboard.Listener(on_release=self._on_release)

    def _on_release(self, key):
        self.logic(key)

    def do_step(self) -> bool:
        self.draw()

        return self.is_active

    def logic(self, key):
        pos_x, pos_y = self.hero.pos_x, self.hero.pos_y

        if key == keyboard.Key.esc:
            self.finish()
            return

        elif key == keyboard.KeyCode.from_char("w") or key == keyboard.Key.up:
            self.hero.pos_y -= 1

        elif key == keyboard.KeyCode.from_char("s") or key == keyboard.Key.down:
            self.hero.pos_y += 1

        elif key == keyboard.KeyCode.from_char("d") or key == keyboard.Key.right:
            self.hero.pos_x += 1

        elif key == keyboard.KeyCode.from_char("a") or key == keyboard.Key.left:
            self.hero.pos_x -= 1

        if (pos_x, pos_y) != (self.hero.pos_x, self.hero.pos_y):
            game_object: GameObject = self.board[self.hero.pos_y][self.hero.pos_x]

            if isinstance(game_object, Wall):  # Если уперлись в стену
                self.hero.pos_x, self.hero.pos_y = pos_x, pos_y
                return

            if isinstance(game_object, Gold):
                self.hero.gold += game_object.value

            self.board[self.hero.pos_y][self.hero.pos_x] = self.hero  # Рисуем героя
            self.board[pos_y][pos_x] = GameObject(
                pos_x, pos_y
            )  # Старое место стало пустым

    def draw(self):
        clear()

        self.draw_board()
        self.draw_game_info()

    def draw_board(self):
        for row in self.board:
            print("".join(game_object.icon for game_object in row))

    def draw_game_info(self):
        print(
            f"Hero: position: {self.hero.pos_x}x{self.hero.pos_y}, gold: {self.hero.gold}"
        )

    def start(self, board_template: str):
        self.is_active = True
        self.board.clear()
        self.listener.start()

        for y, lines in enumerate(board_template.splitlines()):
            self.board.append([])

            for x, value in enumerate(lines):
                match value:
                    case "@":
                        self.hero.pos_x = x
                        self.hero.pos_y = y
                        game_object = self.hero

                    case "G":
                        game_object = Gold(
                            pos_x=x,
                            pos_y=y,
                            value=randint(1, 100),
                        )

                    case "#":
                        game_object = Wall(pos_x=x, pos_y=y)

                    case _:
                        game_object = GameObject(
                            pos_x=x,
                            pos_y=y,
                        )

                self.board[-1].append(game_object)

    def finish(self):
        self.is_active = False
        self.listener.stop()


if __name__ == "__main__":
    game = Game()
    game.start(board_template=BOARD_TEMPLATE)

    while game.do_step():
        time.sleep(0.100)
