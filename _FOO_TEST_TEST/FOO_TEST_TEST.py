#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import multiprocessing as mp
import random
from multiprocessing.pool import Pool

import requests

from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPlainTextEdit

# import crash_python
import crash_on_windows as crash_python


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
)
session = requests.session()
session.headers["User-Agent"] = USER_AGENT

POOL: Pool | None = None


def do_get_process(url: str) -> str:
    crash = random.randint(0, 1) == 1
    print(mp.current_process(), url, f"CRASH={crash}")

    if crash:
        print(mp.current_process(), url, "")
        crash_python.main()

    rs = session.get(url)
    rs.raise_for_status()
    return f"[{rs.status_code}] {rs.url}"


def do_get(url: str) -> str | None:
    print("before apply", url)
    result = POOL.apply_async(do_get_process, args=[url])
    print(result, result._event, result._job, result._pool)
    try:
        return result.get(timeout=60)
    except mp.context.TimeoutError:
        return
    except Exception as e:
        print("after apply error", e, type(e), url)
    finally:
        print("after apply", url)


class RunFuncThread(QThread):
    run_finished = pyqtSignal(object)
    about_error = pyqtSignal(Exception)

    def __init__(self, func):
        super().__init__()

        self.func = func

    def run(self):
        try:
            self.run_finished.emit(self.func())
        except Exception as e:
            self.about_error.emit(e)


class Addon(QWidget):
    def __init__(self, url: str):
        super().__init__()

        self.log = QPlainTextEdit()
        self.log.setWordWrapMode(QTextOption.NoWrap)

        self.url: str = url
        self.n: int = 0

        self.thread_run = RunFuncThread(func=lambda: do_get(url))
        self.thread_run.started.connect(self._started)
        self.thread_run.run_finished.connect(lambda data: self.log.appendPlainText(f"Data: {data}"))
        self.thread_run.about_error.connect(lambda e: self.log.appendPlainText(f"Error: {e}"))
        self.thread_run.finished.connect(lambda: self.log.appendPlainText("Finished\n"))

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.log)

    def refresh(self):
        self.thread_run.start()

    def _started(self):
        self.n += 1
        self.log.appendPlainText(f"[{self.n}] Started {self.url}")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QGridLayout(self)

        self.addons = [
            Addon(url="https://jut.su/mushoku-tensei/season-1/episode-14.html"),
            Addon(url="https://github.com"),
            Addon(url="https://jut.su/"),
            Addon(url="https://ya.ru"),
            Addon(url="https://404"),
            Addon(url="https://ru.wikipedia.org/"),
        ]
        columns: int = 2
        for row, addon in enumerate(self.addons):
            row, col = divmod(row, columns)
            main_layout.addWidget(addon, row, col)

        self.timer = QTimer()
        self.timer.setInterval(5_000)
        self.timer.timeout.connect(self.refresh)
        self.timer.start()

    def refresh(self):
        for addon in self.addons:
            addon.refresh()


if __name__ == "__main__":
    print(mp.current_process())

    with mp.Pool(processes=10) as pool:
        POOL = pool

        app = QApplication([])

        mw = MainWindow()
        mw.show()

        mw.refresh()

        app.exec()
