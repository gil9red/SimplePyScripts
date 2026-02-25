#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Template method — Шаблонный метод
# SOURCE: https://ru.wikipedia.org/wiki/Шаблонный_метод_(шаблон_проектирования)


from abc import ABC, abstractmethod


class GameObject(ABC):
    players_count: int

    def end_of_game(self) -> bool:
        pass

    @abstractmethod
    def initialize_game(self) -> None:
        pass

    @abstractmethod
    def make_play(self, player: int) -> None:
        pass

    @abstractmethod
    def print_winner(self) -> None:
        pass

    # A template method :
    def play_one_game(self, players_count: int) -> None:
        self.players_count = players_count
        self.initialize_game()

        j = 0

        while not self.end_of_game():
            self.make_play(j)
            j = (j + 1) % players_count

        self.print_winner()


# Now we can extend this class in order to implement actual games:
class Monopoly(GameObject):
    # Implementation of necessary concrete methods
    def initialize_game(self) -> None:
        # Initialize money
        ...

    def make_play(self, player: int) -> None:
        # Process one turn of player
        ...

    def end_of_game(self) -> bool:
        return True

    def print_winner(self) -> None:
        # Display who won
        ...

    # Specific declarations for the Monopoly game.
    # ...


class Chess(GameObject):
    # Implementation of necessary concrete methods
    def initialize_game(self) -> None:
        # Put the pieces on the board
        ...

    def make_play(self, player: int) -> None:
        # Process a turn for the player
        ...

    def end_of_game(self) -> bool:
        # Return true if in Checkmate or Stalemate has been reached
        return True

    def print_winner(self) -> None:
        # Display the winning player
        ...

    # Specific declarations for the chess game.
    # ...


if __name__ == "__main__":
    game = Monopoly()
    game.play_one_game(2)

    game = Chess()
    game.play_one_game(2)
