#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path
from textwrap import dedent

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


DIR = Path(__file__).resolve().parent

DIR_OUT = DIR / 'out'
DIR_OUT.mkdir(parents=True, exist_ok=True)


options = Options()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)

try:
    driver.get('https://pikabu.ru/')
    print(f'Title: "{driver.title}"')

    # Содержит иконки в тегах symbol
    svg_app_el = driver.find_element(By.CSS_SELECTOR, 'svg.app-svg')

    # Содержит предустановленные фигуры. Без него некоторые из иконок-эмоций отображались частично
    svg_defs_el = svg_app_el.find_element(By.CSS_SELECTOR, 'defs')
    defs = svg_defs_el.get_attribute('outerHTML')

    # Перебор и сохранение svg с эмоциями
    for svg_symbol_el in svg_app_el.find_elements(By.CSS_SELECTOR, 'symbol'):
        el_id = svg_symbol_el.get_attribute('id')
        if 'icon--emotions__' in el_id:
            svg_symbol = svg_symbol_el.get_attribute('outerHTML')
            svg = dedent(f'''\
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                {defs}
                {svg_symbol}
                <use xlink:href="#{el_id}"/>
            </svg>
            ''')
            file_name = DIR_OUT / f'{el_id}.svg'
            print(f'Saving {file_name} ...')

            file_name.write_text(svg, encoding='utf-8')

finally:
    driver.quit()
