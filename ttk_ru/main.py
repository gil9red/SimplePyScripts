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


URL = "https://lk.ttk.ru/services"


def get_price() -> str:
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, timeout=30)

    try:
        driver.get(URL)
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

            while "/auth" in driver.current_url:
                time.sleep(1)

            # Попытаемся пройти дальше
            driver.get(URL)

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


if __name__ == "__main__":
    print(get_price())
    # 300
