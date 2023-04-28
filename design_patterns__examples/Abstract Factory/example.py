#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Abstract Factory - Абстрактная фабрика
# SOURCE: https://en.wikipedia.org/wiki/Abstract_factory_pattern#Java_example


from abc import ABC, abstractmethod


class IWidget(ABC):
    @abstractmethod
    def paint(self):
        pass


class ILabel(IWidget):
    @abstractmethod
    def paint(self):
        pass


class IButton(IWidget):
    @abstractmethod
    def paint(self):
        pass


class IGUIFactory(ABC):
    @abstractmethod
    def create_label(self) -> ILabel:
        pass

    @abstractmethod
    def create_button(self) -> IButton:
        pass


class WinLabel(ILabel):
    def paint(self):
        print("WinLabel")


class OSXLabel(ILabel):
    def paint(self):
        print("OSXLabel")


class WinButton(IButton):
    def paint(self):
        print("WinButton")


class OSXButton(IButton):
    def paint(self):
        print("OSXButton")


class WinFactory(IGUIFactory):
    def create_label(self) -> ILabel:
        return WinLabel()

    def create_button(self) -> IButton:
        return WinButton()


class OSXFactory(IGUIFactory):
    def create_label(self) -> ILabel:
        return OSXLabel()

    def create_button(self) -> IButton:
        return OSXButton()


if __name__ == "__main__":
    def random_appearance() -> str:
        import random
        return random.choice(["OSX", "Windows", "error"])

    factory = None
    appearance = random_appearance()  # Current operating system

    if appearance == "OSX":
        factory = OSXFactory()

    elif appearance == "Windows":
        factory = WinFactory()

    else:
        raise Exception("No such operating system")

    label = factory.create_label()
    label.paint()

    button = factory.create_button()
    button.paint()
