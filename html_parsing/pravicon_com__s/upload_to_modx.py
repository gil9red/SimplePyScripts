#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import time
import traceback

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from config import DIR_DUMP, URL_MODIX_BASE, URL_MODIX_CREATE, LOGIN, PASSWORD
from main import secure_filename


options = Options()
# options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
try:
    driver.implicitly_wait(5)

    driver.get(URL_MODIX_BASE)
    print(f"Title: {driver.title!r}")

    driver.find_element(By.ID,  "modx-login-username").send_keys(LOGIN)
    driver.find_element(By.ID,  "modx-login-password").send_keys(PASSWORD)

    driver.find_element(By.ID,  "modx-login-btn").click()

    # Папки с сортировкой по имени
    items = sorted(
        DIR_DUMP.glob("icon-*"), key=lambda x: x.stem.split("__", maxsplit=1)[1]
    )

    for i, path_dir in enumerate(items, 1):
        path_ignore = path_dir / "ignore"
        if path_ignore.exists():
            continue

        driver.get(URL_MODIX_CREATE)

        path_info = path_dir / "Информация.json"
        data_info = json.loads(path_info.read_text("utf-8"))

        title = data_info["title"]
        print(f"#{i} / {len(items)}. {title}")

        file_name_img = f"{secure_filename(title)}.jpg"

        driver.find_element(By.ID,  "modx-resource-pagetitle").send_keys(title)

        path_description = path_dir / "Описания иконы.txt"
        description = path_description.read_text("utf-8")
        if "В этом разделе записей пока нет." not in description:
            driver.find_element(By.ID,  "ta").send_keys(description)

        # Тип содержимого JSON
        # driver.find_element_by_css_selector('[name=content_type]').get_attribute()
        driver.execute_script(
            "arguments[0].setAttribute('value', arguments[1])",
            driver.find_element(By.CSS_SELECTOR, "[name=content_type]"),
            "7",  # JSON
        )

        driver.find_element(By.ID,  "modx-resource-tabs__modx-panel-resource-tv").click()
        driver.find_element(By.ID,  "tvbrowser1").send_keys(
            f"manager/иконы святых/{file_name_img}"
        )

        driver.find_element(By.ID,  "tv3").send_keys("Описание")

        path_liturgical_texts = path_dir / "Богослужебные тексты.txt"
        if path_liturgical_texts.exists():
            liturgical_texts = path_liturgical_texts.read_text("utf-8")
            driver.find_element(By.ID,  "tv5").send_keys(liturgical_texts)

        driver.find_element(By.ID,  "modx-abtn-save").click()

        path_ignore.touch()

        time.sleep(5)

except:
    print(traceback.format_exc())

finally:
    # driver.quit()
    pass
