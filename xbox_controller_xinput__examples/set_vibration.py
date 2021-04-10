#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import time
from operator import attrgetter


# SOURCE: https://github.com/r4dian/Xbox-Controller-for-Python/blob/6932394fe5170cb52e9eee4ee601aa9415ed036a/xinput.py
import xinput


joysticks = xinput.XInputJoystick.enumerate_devices()
device_numbers = list(map(attrgetter('device_number'), joysticks))
print('Found %d devices: %s' % (len(joysticks), device_numbers))

if not joysticks:
    sys.exit(0)

j = joysticks[0]
print(j)

j.set_vibration(100, 100)

time.sleep(2)

j.set_vibration(0, 0)
