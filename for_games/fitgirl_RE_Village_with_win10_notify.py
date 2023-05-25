#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as DT
import traceback
import sys

from pathlib import Path

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# pip install simple-wait
from simple_wait import wait

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(
    str(ROOT_DIR / "winapi__windows__ctypes/windows__toast_balloontip_notifications")
)
from run_notify import run_in_thread


def show_notify(name: str):
    title = f"Уведомление за {DT.datetime.now():%Y/%m/%d %H:%M:%S}"
    print(f"{title}\n{name}\n")

    run_in_thread(title, name, duration=10 * 3600)


name = "Resident Evil Village"
URL = f"https://fitgirl-repacks.site/?s={name}"


options = Options()
options.add_argument("--headless")


if __name__ == "__main__":
    while True:
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)

        try:
            driver.get(URL)
            if "DDOS-GUARD" in driver.title.upper():
                driver.refresh()
                print(f"Title: {driver.title!r}")

            for title_el in driver.find_elements_by_css_selector(".entry-title"):
                title = title_el.text.strip()

                if "VILLAGE" in title_el.text.upper():
                    show_notify(title)

            wait(hours=8)

        except:
            print(traceback.format_exc())
            wait(minutes=15)

        finally:
            driver.quit()
