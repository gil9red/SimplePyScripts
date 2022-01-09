#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


class RegistryException(Exception):
    pass


class RegistryKeyNotFoundException(RegistryException):
    def __init__(self, path: str):
        self.path = path

        super().__init__(f"Registry key not found, path='{self.path}'")


class RegistryValueNotFoundException(RegistryException):
    def __init__(self, path: str, name: str):
        self.path = path
        self.name = name

        super().__init__(f"Registry value not found, path='{self.path}', name='{self.name}'")
