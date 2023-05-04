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
    def initialize_game(self):
        pass

    @abstractmethod
    def make_play(self, player: int):
        pass

    @abstractmethod
    def print_winner(self):
        pass

    # A template method :
    def play_one_game(self, players_count: int):
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
    def initialize_game(self):
        # Initialize money
        ...

    def make_play(self, player: int):
        # Process one turn of player
        ...

    def end_of_game(self) -> bool:
        return True

    def print_winner(self):
        # Display who won
        ...

    # Specific declarations for the Monopoly game.
    # ...


class Chess(GameObject):
    # Implementation of necessary concrete methods
    def initialize_game(self):
        # Put the pieces on the board
        ...

    def make_play(self, player: int):
        # Process a turn for the player
        ...

    def end_of_game(self) -> bool:
        # Return true if in Checkmate or Stalemate has been reached
        return True

    def print_winner(self):
        # Display the winning player
        ...

    # Specific declarations for the chess game.
    # ...


if __name__ == "__main__":
    game = Monopoly()
    game.play_one_game(2)

    game = Chess()
    game.play_one_game(2)
