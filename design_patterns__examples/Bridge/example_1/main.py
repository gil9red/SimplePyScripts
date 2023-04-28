#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Bridge — Мост
# SOURCE: https://ru.wikipedia.org/wiki/Мост_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/bridge
# SOURCE: https://refactoring.guru/ru/design-patterns/bridge/java/example


from devices.radio import Radio
from devices.tv import Tv

from remotes.basic_remote import BasicRemote
from remotes.advanced_remote import AdvancedRemote


def test_device(device):
    print("Tests with basic remote.")
    basic_remote = BasicRemote(device)
    basic_remote.power()
    device.print_status()

    print("Tests with advanced remote.")
    advanced_remote = AdvancedRemote(device)
    advanced_remote.power()
    advanced_remote.mute()
    device.print_status()


if __name__ == "__main__":
    test_device(Tv())
    test_device(Radio())
