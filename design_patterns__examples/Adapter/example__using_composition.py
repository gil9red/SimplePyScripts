#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Adapter - Адаптер
# SOURCE: https://ru.wikipedia.org/wiki/Адаптер_(шаблон_проектирования)#Python


from abc import ABC, abstractmethod


class SourceAdapter(ABC):
    @abstractmethod
    def get_picture(self):
        pass


class GameConsole:
    def create_game_picture(self):
        return "picture from console"


class Antenna:
    def create_wave_picture(self):
        return "picture from wave"


class SourceGameConsoleAdapter(SourceAdapter):
    def __init__(self, game_console: GameConsole):
        self.game_console = game_console

    def get_picture(self):
        return self.game_console.create_game_picture()


class SourceAntennaAdapter(SourceAdapter):
    def __init__(self, antenna: Antenna):
        self.antenna = antenna

    def get_picture(self):
        return self.antenna.create_wave_picture()


class TV:
    def __init__(self, source: SourceAdapter):
        self.source = source

    def show_picture(self):
        return self.source.get_picture()


if __name__ == "__main__":
    g = SourceGameConsoleAdapter(GameConsole())
    game_tv = TV(g)
    print(game_tv.show_picture())

    a = SourceAntennaAdapter(Antenna())
    cabel_tv = TV(a)
    print(cabel_tv.show_picture())
