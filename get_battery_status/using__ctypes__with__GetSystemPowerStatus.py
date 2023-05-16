#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.microsoft.com/en-us/windows/desktop/api/winbase/nf-winbase-getsystempowerstatus
# SOURCE: https://docs.microsoft.com/ru-ru/windows/desktop/api/winbase/ns-winbase-_system_power_status


from ctypes import windll, Structure, c_byte, c_ulong, byref


class SystemPowerStatus(Structure):
    _fields_ = [
        ("ACLineStatus", c_byte),
        ("BatteryFlag", c_byte),
        ("BatteryLifePercent", c_byte),
        ("Reserved1", c_byte),
        ("BatteryLifeTime", c_ulong),
        ("BatteryFullLifeTime", c_ulong),
    ]


system_power_status = SystemPowerStatus()
result = windll.kernel32.GetSystemPowerStatus(byref(system_power_status))
print(system_power_status.BatteryLifePercent)
