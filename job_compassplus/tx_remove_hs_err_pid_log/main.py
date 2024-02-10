#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import logging
import time
import sys

from logging.handlers import RotatingFileHandler
from pathlib import Path


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
            file, maxBytes=10_000_000, backupCount=5, encoding=encoding
        )
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log


DIR = Path(__file__).resolve().parent

log = get_logger(
    file=DIR / "deleted.txt",
    formatter="[%(asctime)s] %(message)s",
)


DIRS = [r"C:\DEV__TX", r"C:\DEV__OPTT", r"C:\DEV__RADIX"]


def run(dirs: list[str | Path]):
    print(f"\n{dt.datetime.today()}")

    for dir_path in dirs:
        print(dir_path)
        for file_name in Path(dir_path).glob("*/hs_err_pid*.log"):
            ctime_timestamp = file_name.stat().st_ctime
            ctime = dt.datetime.fromtimestamp(ctime_timestamp)
            ctime = ctime.replace(microsecond=0)

            text = f"{file_name} (date creation: {ctime})"
            print(text)

            # Удаление, если с даты создания прошло больше 1 часа
            if dt.datetime.today() > ctime + dt.timedelta(hours=1):
                log.info(text)
                file_name.unlink(missing_ok=True)


if __name__ == "__main__":
    if "--one" in sys.argv:
        run(DIRS)
        sys.exit()

    while True:
        run(DIRS)
        time.sleep(2 * 60 * 60)
