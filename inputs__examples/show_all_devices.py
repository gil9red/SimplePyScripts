#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time

# pip install inputs
from inputs import DeviceManager


while True:
    devices = DeviceManager()
    print(
        f'keyboards: {len(devices.keyboards)}, mice: {len(devices.mice)}, '
        f'gamepads: {len(devices.gamepads)}, microbits: {len(devices.microbits)}, '
        f'leds: {len(devices.leds)}, other_devices: {len(devices.other_devices)}, '
        f'all_devices: {len(devices.all_devices)}'
    )
    time.sleep(1)
