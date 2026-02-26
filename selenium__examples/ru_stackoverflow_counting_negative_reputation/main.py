#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import time

# pip install selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def get_int(element) -> int:
    value = re.sub(r"\D", "", element.text)
    return int(value)


def scroll_and_click(element, sleep: float = None) -> None:
    driver.execute_script("arguments[0].scrollIntoView()", element)
    element.click()

    if sleep:
        time.sleep(sleep)


def parse_rep_left_value(rep_left_value: str) -> tuple[int, int]:
    rep_up = rep_down = 0
    if rep_left_value:
        if "/" in rep_left_value:
            rep_up, rep_down = map(int, rep_left_value.split("/"))
        else:
            rep_left_value = int(rep_left_value)
            if rep_left_value > 0:
                rep_up = rep_left_value
            else:
                rep_down = rep_left_value

    return rep_up, rep_down


def has_class(class_: str, element) -> bool:
    return class_ in element.get_attribute("class").split()


DEBUG_LOG = False
URL = "https://ru.stackoverflow.com/users/201445/gil9red?tab=reputation"


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(2)

try:
    t = time.perf_counter()

    driver.get(URL)
    print(f'Title: "{driver.title}"')

    time.sleep(2)

    current_rep = get_int(
        driver.find_element(By.CSS_SELECTOR, "#user-tab-reputation .count")
    )
    total_negative_rep_by_user_is_deleted = 0
    total_negative_rep_by_bounty = 0
    total_negative_rep = 0
    max_negative_rep_by_day = 0

    while True:
        for tr in driver.find_elements(
            By.CSS_SELECTOR, "#rep-page-container .rep-table-row"
        ):
            rep_value = get_int(tr.find_element(By.CSS_SELECTOR, ".rep-cell"))

            rep_day_el = tr.find_element(By.CSS_SELECTOR, ".rep-day")
            rep_day_title = rep_day_el.get_attribute("title")
            rep_day_text = rep_day_el.text.strip()

            print(f"{rep_value:4} {rep_day_title} ({rep_day_text})")

            is_expanded = has_class(
                "expander-arrow-small-show",
                rep_day_el.find_element(By.CSS_SELECTOR, ".load-body"),
            )
            if not is_expanded:
                scroll_and_click(rep_day_el, sleep=1.5)

            # От текущего элемента ищем следующий tr с классом loaded-body
            loaded_body_el = tr.find_element(
                By.XPATH, "following-sibling::tr[contains(@class, 'loaded-body')]"
            )
            rep_change_items = loaded_body_el.find_elements(
                By.CSS_SELECTOR, ".rep-breakdown-row"
            )
            if rep_change_items:
                sum_negative_rep = 0

                for rep_row_el in rep_change_items:
                    rep_left_value = rep_row_el.find_element(
                        By.CSS_SELECTOR, ".rep-left"
                    ).text.strip()
                    rep_up, rep_down = parse_rep_left_value(rep_left_value)

                    rep_desc_el = rep_row_el.find_element(By.CSS_SELECTOR, ".rep-desc")
                    rep_desc = rep_desc_el.text.strip()
                    rep_desc_title = rep_desc_el.get_attribute("title")

                    # Для случаев, когда в один день ответ был принят и отозван
                    if rep_up == 15 and rep_down == -15 and rep_desc == "2 события":
                        rep_up = rep_down = 0

                    DEBUG_LOG and print(
                        f"    {rep_left_value:4} ({rep_up}/{rep_down}) : {rep_desc!r} => {rep_desc_title!r}"
                    )

                    if rep_desc_title == "участник был удалён":
                        total_negative_rep_by_user_is_deleted += rep_down

                    if rep_desc_title == "предложено вознаграждение за вопрос":
                        total_negative_rep_by_bounty += rep_down

                    # Если минус был отозван, то плюсуем в сумму минусов
                    if rep_desc_title == "голос против данного сообщения был отозван":
                        total_negative_rep += rep_up

                    total_negative_rep += rep_down
                    sum_negative_rep += rep_down

                if max_negative_rep_by_day > sum_negative_rep:
                    max_negative_rep_by_day = sum_negative_rep

            else:
                # Для случаев, когда нет описания изменения: "В этот день не было суммарного изменения репутации"
                if rep_value < 0:
                    total_negative_rep += rep_value

        # Переход на следующую страницу
        try:
            next_el = driver.find_element(
                By.CSS_SELECTOR, '.s-pagination > [rel="next"]'
            )
            print("[+] Move to next page:", next_el.get_attribute("href"))

            scroll_and_click(next_el, sleep=5)

        except NoSuchElementException:
            print("[+] Last page, stop it.")
            break

    print("\n" + "-" * 100 + "\n")

    # Подсчет репутации с учетом минусов
    max_possible_rep = current_rep + abs(total_negative_rep)

    # Процент минусов от максимально-возможной репутации
    percent_negative_rep = abs(total_negative_rep) * 100 / max_possible_rep

    print(f"Elapsed {int(time.perf_counter() - t)} secs")
    print()
    print("Current reputation:", current_rep)
    print(
        f"Total negative reputation: {total_negative_rep} ({percent_negative_rep:.2f}%)"
    )
    print(
        "    Total negative reputation (user is deleted):",
        total_negative_rep_by_user_is_deleted,
    )
    print("    Total negative reputation (bounty):", total_negative_rep_by_bounty)
    print("Max negative reputation by day:", max_negative_rep_by_day)
    # Elapsed 2299 secs
    #
    # Current reputation: 52894
    # Total negative reputation: -1711 (3.13%)
    #     Total negative reputation (user is deleted): -686
    #     Total negative reputation (bounty): -300
    # Max negative reputation by day: -180

finally:
    driver.quit()
