#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def dict_to_url_params(json_data, root):
    def deep(node, root, items):
        if isinstance(node, list):
            for i, value in enumerate(node):
                node_root = root + f"[{i}]"
                deep(value, node_root, items)

        elif isinstance(node, dict):
            for key, value in node.items():
                node_root = root + f"[{key}]"
                deep(value, node_root, items)

        else:
            root += "=" + node
            items.append(root)

    items = []

    deep(json_data, root, items)

    return items


if __name__ == "__main__":
    JSON_FORM_DATA = {
        "add": [
            {
                "source_name": "WEB сайт",
                "source_uid": "a1fee7c0fc436088e64ba2e8822ba2b3",
                "created_at": "1529007000",
                "incoming_entities": {
                    "leads": [
                        {"name": "Покупка"},
                    ],
                    "contacts": [
                        {
                            "name": "Федя",
                            "responsible_user_id": "1903006",
                            "custom_fields": [
                                {
                                    "id": "382707",
                                    "values": [
                                        {"value": "+77777777777", "enum": "WORK"}
                                    ],
                                },
                                {
                                    "id": "389993",
                                    "values": [{"value": "sfgh3gh233h3h3h3"}],
                                },
                                {
                                    "id": "389995",
                                    "values": [{"value": "Обратный звонок"}],
                                },
                            ],
                        }
                    ],
                },
                "incoming_lead_info": {
                    "form_id": "329248",
                    "form_page": "vdtest.ru",
                    "ip": "127.0.0.1",
                    "service_code": "QkKwSam8",
                },
            }
        ]
    }

    items = dict_to_url_params(JSON_FORM_DATA["add"], root="add")

    params = "&".join(items)
    print("Params: " + params)
    print()

    print("Params:")
    for x in items:
        print(x)
