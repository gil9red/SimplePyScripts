#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import multiprocessing as mp
from multiprocessing.pool import Pool
from typing import Callable, Any

import requests

from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPlainTextEdit,
    QProgressBar,
)


POOL: Pool | None = None


class CustomAdapter(requests.adapters.HTTPAdapter):
    timeout: int = 60
    max_attempts: int = 3

    def send(self, *args, **kwargs) -> requests.Response:
        # Установка таймаута, если оно не было задано
        if not kwargs.get("timeout"):
            kwargs["timeout"] = self.timeout

        # В дочернем процессе будет None
        if POOL:
            last_error: Exception | None = None
            for _ in range(self.max_attempts):
                try:
                    apply = POOL.apply_async(super().send, args=args, kwds=kwargs)
                    return apply.get(timeout=self.timeout)

                except Exception as e:
                    last_error = e

            raise last_error

        print("[CustomAdapter]", mp.current_process(), args[0].url)
        return super().send(*args, **kwargs)


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
)
session = requests.session()
session.headers["User-Agent"] = USER_AGENT
session.mount("https://", CustomAdapter())
session.mount("http://", CustomAdapter())


class RunFuncThread(QThread):
    run_finished = pyqtSignal(object)
    about_error = pyqtSignal(Exception)

    def __init__(self, func: Callable[[], Any]):
        super().__init__()

        self.func: Callable[[], Any] = func

    def run(self):
        try:
            self.run_finished.emit(self.func())
        except Exception as e:
            self.about_error.emit(e)


def do_get(url: str) -> str:
    rs = session.get(url)
    rs.raise_for_status()
    return f"[{rs.status_code}] {rs.url}"


class Addon(QWidget):
    def __init__(self):
        super().__init__()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()

        self.log = QPlainTextEdit()
        self.log.setWordWrapMode(QTextOption.NoWrap)

        self.n: int = 0

        self.thread_run = RunFuncThread(func=self.get_data)
        self.thread_run.started.connect(self._started)
        self.thread_run.run_finished.connect(
            lambda data: self.log.appendPlainText(f"Data: {data}")
        )
        self.thread_run.about_error.connect(
            lambda e: self.log.appendPlainText(f"Error: {e} ({type(e)})")
        )
        self.thread_run.finished.connect(self._finished)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.log)

    def get_data(self) -> Any:
        raise NotImplementedError()

    def refresh(self):
        self.thread_run.start()

    def _started(self):
        self.progress_bar.show()

        self.n += 1
        self.log.appendPlainText(f"[{self.n}] Started")

    def _finished(self):
        self.progress_bar.hide()
        self.log.appendPlainText("Finished\n")


class AddonGetUrl1(Addon):
    def get_data(self) -> Any:
        return do_get("https://jut.su/mushoku-tensei/season-1/episode-14.html")


class AddonGetUrl2(Addon):
    def get_data(self) -> Any:
        return do_get("https://github.com")


class AddonGetUrl3(Addon):
    def get_data(self) -> Any:
        return do_get("https://404")


class AddonGetUrl4(Addon):
    def get_data(self) -> Any:
        # NOTE: 10 - max
        return do_get("https://httpbin.org/delay/10")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QGridLayout(self)

        self.addons = [
            AddonGetUrl1(),
            AddonGetUrl2(),
            AddonGetUrl3(),
            AddonGetUrl4(),
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
        print("\n[REFRESH]")

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
