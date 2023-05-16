#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.microsoft.com/en-us/windows/desktop/cimwin32prov/win32-battery


# pip install wmi
import wmi


w = wmi.WMI()
for battery in w.query("select * from Win32_Battery"):
    print(battery.EstimatedChargeRemaining)
