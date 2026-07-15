#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from textwrap import dedent

# playwright>=1.61.0
from playwright.sync_api import sync_playwright

from human_automation import HumanAutomation


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    human_automation = HumanAutomation(page)

    url: str = "https://translate.google.ru/?sl=ru&tl=en&op=translate"
    page.goto(url, wait_until="domcontentloaded")

    input_locator = page.locator('textarea[aria-label="Исходный текст"]')

    human_automation.type_text(
        input_locator,
        text=dedent("""
            Съешь же ещё этих мягких 
            французских булок, 
            да выпей же чаю
        """).strip(),
    )

    page.wait_for_timeout(2_000)

    human_automation.click('button[aria-label *= "Обратный перевод"]:visible')

    page.wait_for_timeout(2_000)

    human_automation.type_text(
        input_locator,
        text=dedent("""
            The quick brown fox jumps 
            over the lazy dog
        """).strip(),
    )

    page.wait_for_timeout(5_000)
