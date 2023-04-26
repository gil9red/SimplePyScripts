#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install py-cpuinfo
import cpuinfo


info = cpuinfo.get_cpu_info()
print(info["brand_raw"])
# AMD Ryzen 7 3700X 8-Core Processor
