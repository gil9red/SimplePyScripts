#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import re

from collections import defaultdict

import requests


session = requests.session()
session.headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"


def get_api_sk_menu(url: str) -> dict:
    rs = session.get(url)
    rs.raise_for_status()

    data_str = re.search(r"window\.SK\.menu = JSON\.parse\('(.+)'\);", rs.text)
    if not data_str:
        raise Exception('Not found "window.SK.menu"!')

    # Нужно убрать экранирование из текста
    data_str = data_str.group(1).encode("utf-8").decode("unicode_escape")
    data: dict = json.loads(data_str)

    # NOTE: Похоже, там всегда одно ключ-значение, причем, похоже, ключ зависит от города
    # Вытаскиваем первый элемент
    return next(iter(data.values()))


def process_category(
    menu_category: dict,
    parent_menu_name: str,
    id_by_active_menu_categories: dict[int, dict],
    id_by_active_dishes: dict[int, dict],
    dish_id_by_variants: dict[int, list[dict]],
    result: dict[str, list[dict]],
    level=0,
):
    name = menu_category["name"]
    children_type = menu_category["children_type"]
    full_name = f"{parent_menu_name}/{name}" if parent_menu_name else name
    print("    " * level + name + "/")

    if children_type == "categories":
        children = []
        for child in menu_category["children"]:
            if category := id_by_active_menu_categories.get(child["id"]):
                children.append(category)

        children.sort(key=lambda x: x["sort"])

        for category in children:
            process_category(
                category,
                full_name,
                id_by_active_menu_categories,
                id_by_active_dishes,
                dish_id_by_variants,
                result,
                level + 1,
            )

    else:
        dishes = []
        for child in menu_category["children"]:
            if dish := id_by_active_dishes.get(child["id"]):
                dishes.append(dish)
        dishes.sort(key=lambda x: x["sort"])

        for dish in dishes:
            dish_id = dish["id"]

            variations = dish_id_by_variants.get(dish_id)
            if not variations:
                continue

            for variation in variations:
                try:
                    dish_name = dish["name"]
                    # Для блюд с вариантами добавляем вариант к названию
                    if variation["type"] != "none":
                        dish_name = f'{dish_name} ({variation["value"]})'

                    dish_price = variation["price"] // 100

                    # Для блюда с одним вариантом калории будут в самом блюде
                    calories = (
                        dish["calories"]
                        if variation["uses_dish_calories"]
                        else variation["calories"]
                    )
                    if not calories:
                        calories = -1

                    weight = (
                        dish["quantity_value"]
                        if variation["uses_dish_quantity"]
                        else variation["quantity_value"]
                    )
                    if not weight:
                        continue

                    weight = re.sub(r"\d+ шт.*", "", weight)  # Удаление количество штук
                    weight = weight.strip("\\/")
                    weight = int(
                        sum(
                            float(x.replace(",", "."))
                            for x in re.split(r"[\\/±]", weight)
                        )
                    )

                    weight_kind = (
                        dish["quantity_units_short_name"]
                        if variation["uses_dish_quantity"]
                        else variation["quantity_units_short_name"]
                    )

                    title = (
                        f"{dish_name}: {dish_price} р, {weight} {weight_kind}, "
                        f"{calories} ккал, разница {weight / dish_price:.2f}"
                    )
                    print("    " * (level + 1) + title)

                    # TODO: ...
                    result[full_name].append(title)

                except Exception:
                    raise Exception(
                        f"Ошибка при нахождении веса блюда #{dish_id} (вариант #{variation['id']})"
                    )


def get_menu(
    url_or_data: str | dict,
    is_business_lunch: bool = False,
) -> dict[str, list]:
    if isinstance(url_or_data, dict):
        data = url_or_data
    else:
        data = get_api_sk_menu(url_or_data)

    id_by_active_menu_categories = {
        x["id"]: x for x in data["categories"] if x["is_active"]
    }
    id_by_active_dishes = {
        dish["id"]: dish
        for dish in data["dishes"]
        if dish["is_available_in_catalog"]
        and dish["is_available_in_site"]
        and dish["is_available_in_app"]
    }
    dish_id_by_variants = defaultdict(list)
    for variation in data["variations"]:
        if variation["is_active"] and variation["is_available"]:
            dish_id = variation["dish_id"]
            dish_id_by_variants[dish_id].append(variation)

    result = defaultdict(list)

    for menu_category in sorted(
        id_by_active_menu_categories.values(), key=lambda x: x["sort"]
    ):
        if not menu_category["is_root"]:
            continue

        # TODO: метод получения вложенных категорий и блюд (словарь?)
        # TODO: метод получения блюд (список?)
        # TODO: Отдельный метод для получения меню из бизнес-меню
        # TODO: Причем, в бизнес меню разбиение на первое/второе/т.п. уже есть
        if is_business_lunch and not menu_category["is_business_lunch"]:
            continue

        process_category(
            menu_category,
            parent_menu_name="",
            id_by_active_menu_categories=id_by_active_menu_categories,
            id_by_active_dishes=id_by_active_dishes,
            dish_id_by_variants=dish_id_by_variants,
            result=result,
        )

    return result
