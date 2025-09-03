#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random
from abc import ABC, abstractmethod
from typing import Optional


# TODO:
class FinishGameException(Exception):
    pass


class Player(ABC):
    def __init__(self, game: Optional["Game"] = None):  # TODO: Выглядит неуклюже
        self.game: Game | None = game

    @abstractmethod
    def make_move(self):
        pass


class UserPlayer(Player):
    def make_move(self):
        while True:
            try:
                stones = int(
                    input(f"Камни от {self.game.MIN_STONES} до {self.game.MAX_STONES} (камней {self.game.number}): ")
                )
                assert self.game.MIN_STONES <= stones <= self.game.MAX_STONES
                break
            except (ValueError, AssertionError):
                print("Неправильное значение!")
                continue

        self.game.number -= stones  # TODO: Мб пусть через игру будет логика - игрок будет говорить сколько камней возьмет, а игра сама решит кто победил
        if self.game.number <= 0:
            # TODO:
            raise FinishGameException("Компьютер выиграл")


class BotPlayer(Player):
    def make_move(self):
        # TODO: Когда остается минимум камней нужно вручную выбрать правильное, а не рандомно
        #       А то ИИ выглядит как искусственный идиот
        stones = min(self.game.number, random.randint(self.game.MIN_STONES, self.game.MAX_STONES))
        print(f"Компьютер выбрал: {stones}")
        self.game.number -= stones  # TODO: Мб пусть через игру будет логика - игрок будет говорить сколько камней возьмет, а игра сама решит кто победил
        if self.game.number <= 0:
            # TODO:
            raise FinishGameException("Ты выиграл")


class Game:
    MIN_STONES: int = 1
    MAX_STONES: int = 3
    MAX_NUMBER: int = 21

    def __init__(self, player1: Player, player2: Player):
        self.player1: Player = player1
        self.player1.game = self

        self.player2: Player = player2
        self.player2.game = self

        self.number: int = self.MAX_NUMBER

        self.is_finished: bool = False
        self.player1_is_first: bool = True

    # TODO: Методы начала игры
    def start(self):
        self.is_finished = False

        # TODO:
        self.player1_is_first = (input("Ты первый? (y/n): ").lower() or "y") == "y"

    # TODO: Мб счетчик раундов вести и явно писать?
    # TODO: Немного ASCII для удобного просмотра
    def move(self) -> bool:
        print(f"Камней: {self.number}")

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


if __name__ == '__main__':
    game = Game(
        player1=UserPlayer(),
        player2=BotPlayer(),
    )
    game.start()

    while game.move():
        pass
