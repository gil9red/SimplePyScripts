#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

# pip install selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import LOGIN, PASSWORD


URL_V1_LOGIN = "https://lk.ttk.ru/po/login.jsf#/"
URL_V2 = "https://lk.ttk.ru/services"


def get_price_v1() -> str:
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, timeout=30)

    try:
        driver.get(URL_V1_LOGIN)
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


def get_price_v2() -> str:
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, timeout=30)

    try:
        driver.get(URL_V2)
        print(f'Title: "{driver.title}", url: {driver.current_url}')

        if "/auth" in driver.current_url:
            print("Нужно авторизоваться")

            username_el = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]'))
            )
            username_el.send_keys(LOGIN)

            # Кнопка "Продолжить"
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

            # На текущий момент поле пароля показывается после клика на кнопку после ввода логина
            password_el = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
            )
            password_el.send_keys(PASSWORD)

            # Кнопка "Войти"
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

            attempts = 30
            while "/auth" in driver.current_url:
                if attempts == 0:
                    raise Exception("Не удалось покинуть страницу /auth")

                attempts -= 1
                time.sleep(1)

            # Попытаемся пройти дальше
            driver.get(URL_V2)

        print(f'Title: "{driver.title}", url: {driver.current_url}')

        attempts = 30
        while "/services" not in driver.current_url:
            if attempts == 0:
                raise Exception("Не удалось открыть страницу /services")

            attempts -= 1
            time.sleep(1)

        # Попробуем найти тег, у которого будет тег с текстом "Стоимость"
        try:
            div_wrapper_price_el = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[*[text()="Стоимость"]]'))
            )
        except TimeoutException:
            raise Exception(f"Не удалось стоимость! Текущая страница: {driver.current_url}")

        price_str = "".join(c for c in div_wrapper_price_el.text if c.isdigit())
        if not price_str:
            raise Exception("Не удалось получить цену!")

        return price_str

    finally:
        driver.quit()


def get_price() -> str:
    try:
        return get_price_v2()
    except Exception:
        print("Не удалось получить цену из новой версии сайта, пробую на старой")
        return get_price_v1()


if __name__ == "__main__":
    print(get_price())
    # 300
