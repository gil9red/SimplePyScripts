#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def is_enabled(self) -> bool:
        pass

    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def disable(self):
        pass

    @abstractmethod
    def get_volume(self) -> int:
        pass

    @abstractmethod
    def set_volume(self, percent: int):
        pass

    @abstractmethod
    def get_channel(self) -> int:
        pass

    @abstractmethod
    def set_channel(self, channel: int):
        pass

    @abstractmethod
    def print_status(self):
        pass
