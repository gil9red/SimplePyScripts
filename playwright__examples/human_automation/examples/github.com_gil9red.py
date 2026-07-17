#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# playwright>=1.61.0
from playwright.sync_api import sync_playwright

from human_automation.human_automation import HumanAutomation

URL: str = "https://github.com/gil9red"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    human_automation = HumanAutomation(page)

    page.goto(URL, wait_until="domcontentloaded")

    part_url: str = "tab=repositories"

    def click_on_repositories() -> None:
        link_locator = page.locator(f'nav a[href *= "{part_url}"]').first
        human_automation.click(link_locator)

    human_automation.ensure_change_url(
        action=click_on_repositories,
        is_ok_url=lambda url: part_url in url,
    )

    print("\n")
    human_automation.wait(300, 600)

    part_url: str = "/SimplePyScripts"

    def find_repository() -> None:
        find_selector = 'input[placeholder="Find a repository…"]'
        find_locator = page.locator(find_selector)
        human_automation.type_text(find_locator, "SimplePyScripts")

        link_selector = (
            f'#user-repositories-list a[itemprop *= "name"][href *= "{part_url}"]'
        )
        locator = page.locator(link_selector).first

        human_automation.click(locator)

    human_automation.ensure_change_url(
        action=find_repository,
        is_ok_url=lambda url: part_url in url,
    )

    human_automation.wait(300, 600)
    print("\n")

    human_automation.move_mouse_to_center()

    # Step 1: Go /playwright__examples
    part_url: str = "/playwright__examples"

    def click_on_step_1() -> None:
        dir_locator = page.get_by_role("link", name=part_url[1:]).first
        human_automation.click(dir_locator)

    human_automation.ensure_change_url(
        action=click_on_step_1,
        is_ok_url=lambda url: part_url in url,
    )

    print("\n")
    human_automation.wait(300, 600)

    # Step 2: Go /playwright__examples/screenshots
    part_url: str = f"{part_url}/screenshots"

    def click_on_step_2() -> None:
        dir_locator = page.locator(f'a[href$="{part_url}"]:visible').first
        human_automation.click(dir_locator)

    human_automation.ensure_change_url(
        action=click_on_step_2,
        is_ok_url=lambda url: url.endswith(part_url),
    )

    print("\n")
    human_automation.wait(300, 600)

    # Step 3: Go /playwright__examples/screenshots/stealth
    part_url: str = f"{part_url}/stealth"

    def click_on_step_3() -> None:
        dir_locator = page.locator(f'a[href$="{part_url}"]:visible').first
        human_automation.click(dir_locator)

    human_automation.ensure_change_url(
        action=click_on_step_3,
        is_ok_url=lambda url: part_url in url,
    )

    print("\n")
    human_automation.wait(300, 600)

    # Step 4: Go /playwright__examples/screenshots/stealth/stealth_firefox_page.png
    part_url: str = f"{part_url}/stealth_firefox_page.png"

    def click_on_step_4() -> None:
        dir_locator = page.locator(f'a[href$="{part_url}"]:visible').first
        human_automation.click(dir_locator)

    human_automation.ensure_change_url(
        action=click_on_step_4,
        is_ok_url=lambda url: part_url in url,
    )

    print("\n")
    human_automation.wait(300, 600)

    # Download /playwright__examples/screenshots/stealth/stealth_firefox_page.png
    img_locator = page.locator(f'img[src *= "{part_url}"]').first
    print(img_locator)

    img_url: str = img_locator.get_attribute("src")
    full_url: str = page.evaluate(f"new URL('{img_url}', window.location.href).href")
    print(full_url)

    response = page.request.get(full_url)
    img_bytes: bytes = response.body()
    print(f"img_bytes ({len(img_bytes)} bytes): {img_bytes[:50]}...")

    page.wait_for_timeout(2_000)
