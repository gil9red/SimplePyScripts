#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from textwrap import dedent

# playwright>=1.61.0
from playwright.sync_api import Page, sync_playwright

from human_automation.human_automation import HumanAutomation


def get_text(page: Page, lang: str) -> str:
    return "\n".join(
        span.text_content().strip()
        for span in page.locator(f'span[lang="{lang}"] > span > span').all()
    )


URL: str = "https://translate.google.ru/?sl=ru&tl=en&op=translate"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    human_automation = HumanAutomation(page)

    page.goto(URL, wait_until="domcontentloaded")

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

    text: str = get_text(page, lang="en")
    print(f"Text ({len(text)}):\n{text}")

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

    page.wait_for_timeout(2_000)

    text: str = get_text(page, lang="ru")
    print(f"Text ({len(text)}):\n{text}")

    page.wait_for_timeout(5_000)
