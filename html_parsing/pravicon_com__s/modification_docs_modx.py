#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
import time
import traceback
from html import unescape

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from config import URL_MODIX_BASE, URL_MODIX_UPDATE, FILE_NAME_IDS, LOGIN, PASSWORD


IDS = json.loads(FILE_NAME_IDS.read_text('utf-8'))


options = Options()
# options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
try:
    driver.implicitly_wait(5)

    driver.get(URL_MODIX_BASE)
    print(f'Title: {driver.title!r}')

    driver.find_element_by_id('modx-login-username').send_keys(LOGIN)
    driver.find_element_by_id('modx-login-password').send_keys(PASSWORD)

    driver.find_element_by_id("modx-login-btn").click()

    for i, doc_id in enumerate(IDS, 1):
        print(f'#{i} / {len(IDS)}. doc_id={doc_id}')

        url = URL_MODIX_UPDATE + doc_id
        driver.get(url)
        print(f'Title: {driver.title!r}')

        need_save = False

        published_el = driver.find_element_by_id('modx-resource-published')
        if not published_el.get_attribute('checked'):
            published_el.click()
            need_save = True

        # Replaced html entities
        description_el = driver.find_element_by_id('ta')
        description = description_el.get_attribute('value')

        new_description = unescape(description)
        new_description = new_description.replace('"', "'")
        new_description = new_description.replace('\n', '')

        if description != new_description:
            description_el.clear()
            description_el.send_keys(new_description)
            need_save = True

        if need_save:
            driver.find_element_by_id('modx-abtn-save').click()

        time.sleep(5)

        print('\n' + '-' * 100 + '\n')

except:
    print(traceback.format_exc())

finally:
    # driver.quit()
    pass
