#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


# TODO:
class FinishGameException(Exception):
    pass


@dataclass
class Player(ABC):
    name: str
    game: Optional["Game"] = field(repr=False, default=None)

    @abstractmethod
    def is_bot(self) -> bool:
        pass

    @abstractmethod
    def make_move(self):
        pass

    def do_choice(self, stones: int):
        if not self.game:
            return

        print(f"Игрок {self.name!r} выбрал: {stones}")
        self.game.do_choice(self, stones)


class UserPlayer(Player):
    def is_bot(self) -> bool:
        return False

    def make_move(self):
        while True:
            try:
                stones = int(
                    input(
                        f"Камни от {self.game.MIN_STONES} до {self.game.MAX_STONES}: "
                    )
                )
                assert self.game.MIN_STONES <= stones <= self.game.MAX_STONES
                break
            except (ValueError, AssertionError):
                print("Неправильное значение!")
                continue

        self.do_choice(stones)


class BotPlayer(Player):
    def is_bot(self) -> bool:
        return True

    def make_move(self):
        # TODO: Когда остается минимум камней нужно вручную выбрать правильное, а не рандомно
        #       А то ИИ выглядит как искусственный идиот
        stones = min(
            self.game.stones, random.randint(self.game.MIN_STONES, self.game.MAX_STONES)
        )
        self.do_choice(stones)


@dataclass
class Game:
    player1: Player
    player2: Player

    round: int = 0
    stones: int = 0
    is_finished: bool = False
    player1_is_first: bool = True

    MIN_STONES: int = 1
    MAX_STONES: int = 3
    MAX_NUMBER: int = 21

    def start(self):
        self.player1.game = self
        self.player2.game = self

        self.round = 0
        self.stones = self.MAX_NUMBER

        self.is_finished = False

        # TODO:
        self.player1_is_first = (input("Ты первый? (y/n): ").lower() or "y") == "y"

    def do_choice(self, player: Player, stones: int):
        self.stones -= stones
        if self.stones <= 0:
            # TODO:
            raise FinishGameException(f"Игрок {player.name!r} проиграл!")

    # TODO: Немного ASCII для удобного просмотра
    def move(self) -> bool:
        self.round += 1

        print(f"Раунд #{self.round}. Камней: {self.stones}")

        try:
            if self.player1_is_first:
                self.player1.make_move()
                self.player2.make_move()
            else:
                self.player2.make_move()
                self.player1.make_move()

        except FinishGameException as e:
            print(e)
            self.is_finished = True

        print()

        return not self.is_finished


if __name__ == "__main__":
    game = Game(
        player1=UserPlayer("Человек"),
        player2=BotPlayer("Бот"),
    )
    game.start()

    while game.move():
        pass
