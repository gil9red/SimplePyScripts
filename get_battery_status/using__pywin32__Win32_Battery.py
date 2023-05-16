#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.microsoft.com/en-us/windows/desktop/cimwin32prov/win32-battery


# pip install pywin32
from win32com.client import GetObject


WMI = GetObject("winmgmts:")
for battery in WMI.InstancesOf("Win32_Battery"):
    print(battery.EstimatedChargeRemaining)
