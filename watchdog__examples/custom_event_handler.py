#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/gorakhargosh/watchdog


import logging
import time
from pathlib import Path

# pip install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# NOTE: It will probably be more functional to inherit
# from RegexMatchingEventHandler or PatternMatchingEventHandler
class CustomEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        super().on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        print(f"Moved {what}: from {event.src_path} to {event.dest_path}")

    def on_created(self, event):
        super().on_created(event)

        what = 'directory' if event.is_directory else 'file'
        print(f"Created {what}: {event.src_path}")

    def on_deleted(self, event):
        super().on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        print(f"Deleted {what}: {event.src_path}")

    def on_modified(self, event):
        super().on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        print(f"Modified {what}: {event.src_path}")


path = Path(__file__).resolve().parent

event_handler = CustomEventHandler()

observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
