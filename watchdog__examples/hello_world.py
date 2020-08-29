#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gorakhargosh/watchdog


import logging
import time
from pathlib import Path

# pip install watchdog
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

path = Path(__file__).resolve().parent

event_handler = LoggingEventHandler()

observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
