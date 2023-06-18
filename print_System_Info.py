#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/Pure-L0G1C/FleX/blob/da8f30f9204a65df57063ed74b3e79a2a79a7bfc/payload/modules/sysinfo.py


from getpass import getuser
from platform import system, release, version, architecture, machine


system_info = {
    "System": system(),
    "Release": release(),
    "Version": version(),
    "Machine": machine(),
    "Username": getuser(),
    "Architecture": architecture()[0],
}
print(system_info)
