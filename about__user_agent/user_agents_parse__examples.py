#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/selwin/python-user-agents


# pip install user-agents
from user_agents import parse


ua_string = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/61.0.3347.109 Safari/537.36"
)
user_agent = parse(ua_string)

print(user_agent)
# PC / Windows 10 / Chrome 61.0.3347

print()

# Accessing user agent's browser attributes
print(user_agent.browser)
print(user_agent.browser.family)
print(user_agent.browser.version)
print(user_agent.browser.version_string)
# Browser(family='Chrome', version=(61, 0, 3347), version_string='61.0.3347')
# Chrome
# (61, 0, 3347)
# 61.0.3347

print()

# Accessing user agent's operating system properties
print(user_agent.os)
print(user_agent.os.family)
print(user_agent.os.version)
print(user_agent.os.version_string)
# OperatingSystem(family='Windows', version=(10,), version_string='10')
# Windows
# (10,)
# 10

print()

# Accessing user agent's device properties
print(user_agent.device)
print(user_agent.device.family)
print(user_agent.device.brand)
print(user_agent.device.model)
# Device(family='Other', brand=None, model=None)
# Other
# None
# None

print()

print(user_agent.is_mobile)
print(user_agent.is_tablet)
print(user_agent.is_touch_capable)
print(user_agent.is_pc)
print(user_agent.is_bot)
# False
# False
# False
# True
# False
