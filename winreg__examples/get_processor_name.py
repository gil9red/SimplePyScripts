#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import RegistryKey


PATH = r"HKLM\HARDWARE\DESCRIPTION\System\CentralProcessor\0"


processor_name: str = RegistryKey.get_or_none(PATH).get_str_value("ProcessorNameString")
print(processor_name)
# Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz
