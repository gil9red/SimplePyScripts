#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# NOTE: https://datatables.net/manual/server-side


import json
import re
from functools import cmp_to_key
from pathlib import Path
from typing import Any

from flask import Flask, render_template, jsonify, Response, request

# pip install querystring-parser==1.2.4
from querystring_parser import parser


def cmp(a: Any, b: Any) -> int:
    return (a > b) - (a < b)


ITEMS = json.load(open("items.json", encoding="utf-8"))


app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template(
        "index.html",
        title=Path(__file__).resolve().parent.name,
    )


@app.route("/api/get_items")
def api_get_items() -> Response:
    args: dict[str, Any] = parser.parse(request.query_string)

    search_value: str = args["search"]["value"]
    has_search_regex: str = args["search"]["regex"] == "true"

    # TODO: Фильтрация может быть по отдельным столбцам в поле search
    #       {
    #           0: {'data': 'id', 'name': 'id', 'searchable': 'true', 'orderable': 'true', 'search': {'value': '', 'regex': 'false'}},
    #           1: {'data': 'name', 'name': 'name', 'searchable': 'true', 'orderable': 'true', 'search': {'value': '', 'regex': 'false'}},
    #           2: {'data': 'description', 'name': 'description', 'searchable': 'true', 'orderable': 'true', 'search': {'value': '', 'regex': 'false'}},
    #           3: {'data': 'command', 'name': 'command', 'searchable': 'true', 'orderable': 'true', 'search': {'value': '', 'regex': 'false'}}
    #       }
    # columns: dict[int, dict[str, str]] = args["columns"]
    print("columns:", args["columns"])

    filtered_items: list[dict[str, Any]] = []
    for item in ITEMS:
        if search_value:
            values: list[str] = [str(x).lower() for x in item.values()]
            if not any(
                (
                    re.search(search_value, value)
                    if has_search_regex
                    else search_value.lower() in value
                )
                for value in values
            ):
                continue

        filtered_items.append(item)

    number_of_filtered = len(filtered_items)

    order: dict[int, dict[str, str]] = args.get("order", dict())
    print("order:", order)
    if order:
        def cmp2(item1: dict[str, str], item2: dict[str, str]) -> int:
            # NOTE: https://stackoverflow.com/a/62381089/5909792
            total_result: int | None = None
            for order_column in order.values():
                name: str = order_column["name"]
                result = cmp(item1[name], item2[name])
                if order_column["dir"] == "desc":
                    result = -result

                if total_result is None:
                    total_result = result
                else:
                    total_result = total_result or result

            return total_result

        filtered_items.sort(key=cmp_to_key(cmp2))

    start: int = int(args["start"])
    length: int = int(args["length"])
    if length > 0:
        filtered_items = filtered_items[start : start + length]

    return jsonify(
        {
            "draw": int(args["draw"]),
            "recordsTotal": len(ITEMS),
            "recordsFiltered": number_of_filtered,
            "data": filtered_items,
        }
    )


if __name__ == "__main__":
    app.run()
