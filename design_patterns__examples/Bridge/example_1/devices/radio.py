#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from devices.device import Device


class Radio(Device):
    def __init__(self) -> None:
        self._on = False
        self._volume = 30
        self._channel = 1

    def is_enabled(self) -> bool:
        return self._on

    def enable(self) -> None:
        self._on = True

    def disable(self) -> None:
        self._on = False

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, volume: int) -> None:
        if volume > 100:
            self._volume = 100
        elif volume < 0:
            self._volume = 0
        else:
            self._volume = volume

    def get_channel(self) -> int:
        return self._channel

    def set_channel(self, channel: int) -> None:
        self._channel = channel

    def print_status(self) -> None:
        print("------------------------------------")
        print("| I'm radio.")
        print("| I'm " + ("enabled" if self._on else "disabled"))
        print("| Current volume is " + str(self._volume) + "%")
        print("| Current channel is " + str(self._channel))
        print("------------------------------------\n")
