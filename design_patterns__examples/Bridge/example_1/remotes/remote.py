#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from abc import ABC, abstractmethod


class Remote(ABC):
    @abstractmethod
    def power(self):
        pass

    @abstractmethod
    def volume_down(self):
        pass

    @abstractmethod
    def volume_up(self):
        pass

    @abstractmethod
    def channel_down(self):
        pass

    @abstractmethod
    def channel_up(self):
        pass
