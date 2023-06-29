#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
import time
from pathlib import Path

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


URL = "https://haveibeenpwned.com"


def do_check(
    email: str,
    dir_save_pwned_screenshots: str = None,
    file_format: str = "%Y-%m-%d %H-%M-%S.png",
) -> str:
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(20)
    try:
        url = f"{URL}/account/{email}"
        print(f"Load {url}")

        driver.get(url)
        print(f"Title: {driver.title!r}")

        time.sleep(5)

        pwned_website_banner = driver.find_element(
            By.CSS_SELECTOR, "#pwnedWebsiteBanner .pwnTitle"
        )
        if pwned_website_banner.is_displayed():
            result = pwned_website_banner.text

            if dir_save_pwned_screenshots:
                dir_screenshots = Path(dir_save_pwned_screenshots)
                dir_screenshots.mkdir(parents=True, exist_ok=True)

                file_name = str(
                    dir_screenshots / dt.datetime.today().strftime(file_format)
                )
                driver.save_screenshot(file_name)

        else:
            result = driver.find_element(By.CSS_SELECTOR, "#noPwnage .pwnTitle").text

        result = " ".join(
            result.strip()
            .replace(" (subscribe to search sensitive breaches)", "")
            .splitlines()
        )
        return result

    finally:
        driver.quit()


if __name__ == "__main__":
    print(do_check("ilya.petrash@inbox.ru"))
    # Oh no — pwned! Pwned on 1 breached site and found no pastes

    print(do_check("e0a545bd9f4a4267baebbba8102fa33a@gmail.com"))
    # Good news — no pwnage found! No breached accounts and no pastes

    print(do_check("foo@gmail.com"))
    # Oh no — pwned! Pwned on 55 breached sites and found 12 pastes
