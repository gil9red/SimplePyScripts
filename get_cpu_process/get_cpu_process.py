#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SOURCE: https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/


import datetime as DT

# pip install psutil
import psutil

from typing import Optional


class ProcessNotFound(Exception):
    def __init__(self, name: str):
        super().__init__(f"Process {name!r} not found")


def find_process(process_name: str) -> Optional[psutil.Process]:
    for process in psutil.process_iter():
        if process_name.lower() == process.name().lower():
            return process

    raise ProcessNotFound(process_name)


def is_running(provided_process_name: str) -> bool:
    """
    Takes the name of a process and
    returns True if it is running,
    False if it isn't
    """

    return bool(find_process(provided_process_name))


def get_pid(provided_process_name: str) -> int:
    """
    Takes the name of a process and
    returns the process id if it
    is running
    """
    return find_process(provided_process_name).pid


def get_process_run_time(provided_process_name: str) -> str:
    """
    Takes the name of a process and
    returns the process runtime
    """
    process = find_process(provided_process_name)

    epoch_created_time = process.create_time()
    dt_created_time = DT.datetime.fromtimestamp(epoch_created_time)
    time_elapsed = DT.datetime.now() - dt_created_time
    return str(time_elapsed).rsplit(".")[0]
