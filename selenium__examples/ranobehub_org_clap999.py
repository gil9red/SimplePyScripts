#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import traceback
import sys
from random import randint

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By


URL = "https://ranobehub.org"
URL_LOGIN = f"{URL}/login"
URL_VOLUME = f"{URL}/ranobe/92/6/4"

MAX_CLAPS = 999
LOGIN = ""
PASSWORD = ""


if not LOGIN or not PASSWORD:
    print("LOGIN and PASSWORD must be defined!")
    sys.exit()


options = Options()
# options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
try:
    driver.implicitly_wait(5)

    driver.get(URL)
    print(f"Title: {driver.title!r}")

    driver.get(URL_LOGIN)
    print(f"Title: {driver.title!r}")

    driver.find_element(By.NAME, "email").send_keys(LOGIN)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    driver.get(URL_VOLUME)
    print(f"Title: {driver.title!r}")

    clap_el = driver.find_element(By.ID, "app-clap-button")
    clap_counter_el = clap_el.find_element(By.CLASS_NAME, "total-counter")

    # Scroll to
    driver.execute_script("arguments[0].scrollIntoView();", clap_el)

    run = True
    while run:
        # Wait clap_counter_el
        while True:
            try:
                total_counter = int(clap_counter_el.text.strip())
                print("Total counter:", total_counter)
                break

            except ValueError:
                time.sleep(5)
                continue

        if total_counter >= MAX_CLAPS:
            break

        clap = randint(8, 25)
        print("Clap:", clap)

        for _ in range(clap):
            try:
                total_counter = int(clap_counter_el.text.strip())
                if total_counter >= MAX_CLAPS:
                    run = False
                    break

                clap_el.click()
                time.sleep(0.033)

            except (ValueError, ElementClickInterceptedException):
                time.sleep(5)
                continue

            except:
                print(traceback.format_exc())

        if not run:
            break

        timeout = randint(20, 60)
        print(f"Timeout: {timeout}\n")

        time.sleep(timeout)

except:
    print(traceback.format_exc())

finally:
    time.sleep(5)
    driver.quit()
