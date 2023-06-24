#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
from urllib.request import urlopen


def get_geolocation() -> dict:
    # SOURCE: https://github.com/Pure-L0G1C/FleX/blob/da8f30f9204a65df57063ed74b3e79a2a79a7bfc/payload/modules/geo.py
    location = {
        "Ip": None,
        "Country": None,
        "City": None,
        "State": None,
        "Zipcode": None,
        "Timezone": None,
        "Latitude": None,
        "Longitude": None,
        "GoogleMapsLink": None,
    }

    try:
        rs = urlopen("http://ip-api.com/json").read()
        data = json.loads(rs, encoding="utf-8")

        location["Ip"] = data["query"]
        location["Country"] = data["country"]

        location["City"] = data["city"]
        location["State"] = data["regionName"]

        location["Zipcode"] = data["zip"]
        location["Timezone"] = data["timezone"]

        location["Latitude"] = data["lat"]
        location["Longitude"] = data["lon"]

        # SOURCE: https://github.com/maldevel/IPGeoLocation/blob/master/core/IpGeoLocation.py#L97
        link = "http://www.google.com/maps/place/{0},{1}/@{0},{1},16z".format(
            location["Latitude"], location["Longitude"]
        )
        location["GoogleMapsLink"] = link

    except:
        pass

    return location


if __name__ == "__main__":
    print(get_geolocation())
