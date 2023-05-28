__author__ = "ipetrash"


import json


if __name__ == "__main__":
    # Compact encoding:
    print(json.dumps([1, 2, 3, {"4": 5, "6": 7}]))

    # Custom separators:
    print(json.dumps([1, 2, 3, {"4": 5, "6": 7}], separators=(",", ":")))

    # Pretty print:
    print(json.dumps([1, 2, 3, {"4": 5, "6": 7}], indent=4))

    # Sort key:
    print(
        json.dumps(["z", "b", "d", {"b": 5, "a": 7, "c": 2}], sort_keys=True, indent=4)
    )

    # Create object:
    obj = [
        3,
        2,
        1,
        [2, 1, 1, 4],
        {
            "a": 1,
            "b": 2,
            "c": 3,
        },
    ]
    print(obj)

    # Obj -> Json string
    str_json_obj = json.dumps(obj, sort_keys=True, indent=4)
    print(str_json_obj)

    # Json string -> Obj
    obj2 = json.loads(str_json_obj)
    print(obj2)

    # Test:
    print(obj2[3][0])
    print(obj2[4]["c"])
    print(obj2[4]["b"])
