#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from remotes.basic_remote import BasicRemote


class AdvancedRemote(BasicRemote):
    """Улучшенный пульт"""

    def mute(self):
        print("Remote: mute")
        self._device.set_volume(0)
