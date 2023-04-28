#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from .device import Device


class Tv(Device):
    def __init__(self):
        self._on = False
        self._volume = 30
        self._channel = 1

    def is_enabled(self) -> bool:
        return self._on

    def enable(self):
        self._on = True

    def disable(self):
        self._on = False

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, volume: int):
        if volume > 100:
            self._volume = 100
        elif volume < 0:
            self._volume = 0
        else:
            self._volume = volume

    def get_channel(self) -> int:
        return self._channel

    def set_channel(self, channel: int):
        self._channel = channel

    def print_status(self):
        print("------------------------------------")
        print("| I'm TV set.")
        print("| I'm " + ("enabled" if self._on else "disabled"))
        print("| Current volume is " + str(self._volume) + "%")
        print("| Current channel is " + str(self._channel))
        print("------------------------------------\n")
