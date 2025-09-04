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
    def make_choice(self) -> int:
        pass


class UserPlayer(Player):
    def is_bot(self) -> bool:
        return False

    def make_choice(self) -> int:
        while True:
            try:
                stones = int(
                    input(
                        f"Игрок {self.name!r} выбирает камни от {self.game.MIN_STONES} до {self.game.MAX_STONES} "
                        f"(всего камней: {self.game.stones}): "
                    )
                )
                assert self.game.MIN_STONES <= stones <= self.game.MAX_STONES

                if stones > self.game.stones:
                    print("Нельзя камней выбрать больше, чем осталось!")
                    continue

                return stones
            except (ValueError, AssertionError):
                print("Неправильное значение!")
                continue


class BotPlayer(Player):
    def is_bot(self) -> bool:
        return True

    def make_choice(self) -> int:
        # Чтобы бот не выбирал очевидно проигрышное количество камней, когда можно победить
        # Если осталось от 2 до 4 камней, то выбирать от 1 до 3 камней - чтобы остался только 1 камень
        match self.game.stones:
            case 1:
                return 1  # Без вариантов, остается только проиграть
            case 2:
                return 1
            case 3:
                return 2
            case 4:
                return 3

        return min(
            self.game.stones,
            random.randint(self.game.MIN_STONES, self.game.MAX_STONES),
        )


@dataclass
class Game:
    player1: Player
    player2: Player

    round: int = 0
    stones: int = 0
    is_finished: bool = False

    MIN_STONES: int = 1
    MAX_STONES: int = 3
    MAX_NUMBER: int = 21

    def start(self):
        self.player1.game = self
        self.player2.game = self

        self.round = 0
        self.stones = self.MAX_NUMBER

        self.is_finished = False

        player1_is_first: bool = False
        variants: list[str] = ["y", "n"]

        if self.player1.is_bot():
            print(f"Игрок {self.player1.name!r} подкидывает монетку")
            player1_is_first = random.choice(variants) == variants[0]
        else:
            while True:
                try:
                    value: str = input(f"Ты первый? ({'/'.join(variants)}): ").lower()
                    if not value:
                        value = variants[0]
                    assert value in variants
                    player1_is_first = value == variants[0]
                    break

                except AssertionError:
                    print("Неправильное значение!")
                    continue

        # Меняем местами первого и второго игроков
        if not player1_is_first:
            self.player1, self.player2 = self.player2, self.player1

        print(f"Первым ходит игрок {self.player1.name!r}")

    def do_choice(self, player: Player):
        stones: int = player.make_choice()
        print(f"Игрок {player.name!r} выбрал: {stones}")

        self.stones -= stones
        if self.stones <= 0:
            # TODO:
            raise FinishGameException(f"Игрок {player.name!r} проиграл!")

    # TODO: Немного ASCII для удобного просмотра
    def move(self) -> bool:
        self.round += 1

        print(f"\nРаунд #{self.round}. Камней: {self.stones}")

        try:
            self.do_choice(self.player1)
            self.do_choice(self.player2)

        except FinishGameException as e:
            print()
            print(e)
            self.is_finished = True

        return not self.is_finished


if __name__ == "__main__":
    game = Game(
        player1=UserPlayer("Человек"),
        player2=BotPlayer("Бот"),
    )
    game.start()

    while game.move():
        pass
