#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# NOTE: Run as administrator


import os

# pip install pythonnet
import clr

from OpenHardwareMonitor import Hardware


openhardwaremonitor_hwtypes = [
    "Mainboard",
    "SuperIO",
    "CPU",
    "RAM",
    "GpuNvidia",
    "GpuAti",
    "TBalancer",
    "Heatmaster",
    "HDD",
]
openhardwaremonitor_sensortypes = [
    "Voltage",
    "Clock",
    "Temperature",
    "Load",
    "Fan",
    "Flow",
    "Control",
    "Level",
    "Factor",
    "Power",
    "Data",
    "SmallData",
]


def initialize_openhardwaremonitor():
    DIR = os.path.abspath(os.path.dirname(__file__))
    dll_file_name = DIR + R"\OpenHardwareMonitorLib.dll"
    clr.AddReference(dll_file_name)

    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle


def fetch_stats(handle) -> None:
    for i in handle.Hardware:
        i.Update()

        for sensor in i.Sensors:
            parse_sensor(sensor)

        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor)


def parse_sensor(sensor) -> None:
    if sensor.Value is None:
        return

    # If SensorType is Temperature
    if sensor.SensorType == openhardwaremonitor_sensortypes.index("Temperature"):
        type_name = openhardwaremonitor_hwtypes[sensor.Hardware.HardwareType]
        print(
            f"    {type_name}. {sensor.Hardware.Name!r} "
            f"Temperature Sensor #{sensor.Index} {sensor.Name} - {sensor.Value}°C"
        )


if __name__ == "__main__":
    print("OpenHardwareMonitor:")
    HardwareHandle = initialize_openhardwaremonitor()
    fetch_stats(HardwareHandle)
