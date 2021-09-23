#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.windxp.com.ru/autrun.htm
# SOURCE: http://www.infosecurity.ru/_gazeta/content/090904/art3.shtml


import os

from dataclasses import dataclass
from typing import Dict, List
from winreg import QueryInfoKey, EnumValue

from get_startup_paths import get_key


PATHS = [
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce",

    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup",
    r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup",

    r"HKEY_CURRENT_USER\Software\Microsoft\WindowsNT\CurrentVersion\Windows\load",
    r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsNT\CurrentVersion\Winlogon\Userinit",
    r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnceEx",
]


@dataclass
class RegistryValue:
    name: str
    value: str
    type: int


def get_run_paths(expand_vars=True) -> Dict[str, List[RegistryValue]]:
    path_by_values = dict()

    for path in PATHS:
        if path not in path_by_values:
            path_by_values[path] = []

        key = get_key(path)
        if not key:
            continue

        _, number_of_values, _ = QueryInfoKey(key)
        for i in range(number_of_values):
            name, value, type_value = EnumValue(key, i)
            value = str(value)
            if expand_vars:
                value = os.path.expandvars(value)

            path_by_values[path].append(
                RegistryValue(name, value, type_value)
            )

    return path_by_values


if __name__ == '__main__':
    run_paths = get_run_paths()
    for path, values in run_paths.items():
        print(path)

        for i, value in enumerate(values, 1):
            print(f'    {i}. {value.name}: {value.value}')

        print()
    r"""
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
        1. Lync: "C:\Program Files (x86)\Microsoft Office\Office15\lync.exe" /fromrunkey
        2. Zoom: "C:\Users\IPetrash\AppData\Roaming\Zoom\bin\Zoom.exe"
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
        1. RTHDVCPL: "C:\Program Files\Realtek\Audio\HDA\RtkNGUI64.exe" -s
        2. DocFetcher-Daemon: C:\Program Files (x86)\DocFetcher\docfetcher-daemon-windows.exe
        3. egui: "C:\Program Files\ESET\ESET Security\ecmds.exe" /run /hide /proxy
        4. SecurityHealth: C:\Program Files\Windows Defender\MSASCuiL.exe
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices
    
    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup
    
    HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup

    """