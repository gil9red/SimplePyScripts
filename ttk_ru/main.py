#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import LOGIN, PASSWORD


URL_LOGIN = "https://lk.ttk.ru/po/login.jsf#/"


def get_price() -> str:
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, timeout=30)

    try:
        driver.get(URL_LOGIN)
        print(f'Title: "{driver.title}", url: {driver.current_url}')

        username_el = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]'))
        )
        username_el.send_keys(LOGIN)

        password_el = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
        )
        password_el.send_keys(PASSWORD)

        while "login" in driver.current_url:
            driver.find_element(By.ID, "submit").click()
            time.sleep(1)

        print(f'Title: "{driver.title}", url: {driver.current_url}')

        css_path = '[services="services.internet"][account="selectedAccount"] [ng-show*="tariffPrice"]'
        price_internet_el = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_path))
        )

        # Waiting for the price to be shown
        attempts = 60
        price_str = None
        for _ in range(attempts):
            # Scrolling to an element so it generates text
            driver.execute_script("arguments[0].scrollIntoView();", price_internet_el)

            price_str = "".join(c for c in price_internet_el.text if c.isdigit())
            if price_str:
                break

            time.sleep(1)

        if not price_str:
            raise Exception("Не удалось получить цену!")

        return price_str

    finally:
        driver.quit()


if __name__ == "__main__":
    print(get_price())
    # 300
