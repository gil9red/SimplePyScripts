#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Strategy — Стратегия
# SOURCE: https://ru.wikipedia.org/wiki/Стратегия_(шаблон_проектирования)
# SOURCE: https://javarush.ru/groups/posts/584-patternih-proektirovanija


from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def download(self, file: str):
        pass


class DownloadWindowsStrategy(Strategy):
    def download(self, file: str):
        print("Windows download: " + file)


class DownloadLinuxStrategy(Strategy):
    def download(self, file: str):
        print("Linux download: " + file)


class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy

    def download(self, file: str):
        self._strategy.download(file)


if __name__ == "__main__":
    context = Context(DownloadWindowsStrategy())
    context.download("file.txt")  # Windows download: file.txt
    print()

    context = Context(DownloadLinuxStrategy())
    context.download("file.txt")  # Linux download: file.txt

    context.set_strategy(DownloadWindowsStrategy())
    context.download("file.txt")  # Windows download: file.txt
