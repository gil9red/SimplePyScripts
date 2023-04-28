#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from remotes.remote import Remote
from devices.device import Device


class BasicRemote(Remote):
    """Стандартный пульт"""

    def __init__(self, device: Device):
        self._device = device

    def power(self):
        print("Remote: power toggle")
        if self._device.is_enabled():
            self._device.disable()
        else:
            self._device.enable()

    def volume_down(self):
        print("Remote: volume down")
        self._device.set_volume(self._device.get_volume() - 10)

    def volume_up(self):
        print("Remote: volume up")
        self._device.set_volume(self._device.get_volume() + 10)

    def channel_down(self):
        print("Remote: channel down")
        self._device.set_channel(self._device.get_channel() - 1)

    def channel_up(self):
        print("Remote: channel up")
        self._device.set_channel(self._device.get_channel() + 1)
