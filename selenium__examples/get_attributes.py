#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install selenium
from selenium import webdriver


def get_attributes(driver, element) -> dict:
    return driver.execute_script(
        """
        let attr = arguments[0].attributes;
        let items = {}; 
        for (let i = 0; i < attr.length; i++) {
            items[attr[i].name] = attr[i].value;
        }
        return items;
        """,
        element,
    )


driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get("https://ru.stackoverflow.com/")

input_el = driver.find_element_by_css_selector("input.s-input__search")
attrs = get_attributes(driver, input_el)
print(attrs)
# {'aria-controls': 'top-search', 'aria-label': 'Поиск', 'autocomplete': 'off',
#  'class': 's-input s-input__search js-search-field ', 'data-action': 'focus->s-popover#show',
#  'data-controller': 's-popover', 'data-s-popover-placement': 'bottom-start', 'maxlength': '240',
#  'name': 'q', 'placeholder': 'Поиск...', 'type': 'text', 'value': ''}

driver.quit()
