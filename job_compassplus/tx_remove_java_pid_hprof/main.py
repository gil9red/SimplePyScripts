#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import logging
import time
import sys

from logging.handlers import RotatingFileHandler
from pathlib import Path

# pip install humanize
from humanize import naturalsize as sizeof_fmt


def get_logger(
    name=__file__,
    file: str | Path = "log.txt",
    formatter: str = "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s",
    encoding="utf-8",
    log_stdout=True,
    log_file=True,
):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(formatter)

    if log_file:
        fh = RotatingFileHandler(
            file, maxBytes=10000000, backupCount=5, encoding=encoding
        )
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


DIR = Path(__file__).resolve().parent
DIRS = [r"C:\DEV__TX", r"C:\DEV__OPTT", r"C:\DEV__RADIX"]


log = get_logger(
    file=DIR / "deleted.txt",
    formatter="[%(asctime)s] %(message)s",
)


def run(dirs: list[str | Path]):
    print(f"\n{dt.datetime.today()}")

    for dir_path in dirs:
        print(dir_path)
        path = Path(dir_path)

        files = list(path.glob("*/*.hprof"))
        files += list(path.rglob(r"*/.config\var\log\heapdump.hprof.old"))
        for f in files:
            ctime_timestamp = f.stat().st_ctime
            ctime = dt.datetime.fromtimestamp(ctime_timestamp)
            ctime = ctime.replace(microsecond=0)

            file_size = f.stat().st_size

            text = f"{f} (date creation: {ctime}, size: {sizeof_fmt(file_size)})"
            print(text)

            # Удаление, если с даты создания прошло больше 1 часа
            if dt.datetime.today() > ctime + dt.timedelta(hours=1):
                log.info(text)
                f.unlink(missing_ok=True)


if __name__ == "__main__":
    while True:
        run(DIRS)
        time.sleep(2 * 60 * 60)
