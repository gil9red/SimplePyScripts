#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import pandas as pd


json_str = """\
{
  "d": {
    "Summary": {
      "TotalCount": 93977,
      "__type": "SelectSummary:#FonbetEngine.DAL"
    },
    "Items": [
      {
        "MaxResult": 6,
        "CouponCode": "10000",
        "TotalPrizeValue": 10
      },
      {
        "MaxResult": 2,
        "CouponCode": "100002",
        "TotalPrizeValue": 90
      },
      {
        "MaxResult": 3,
        "CouponCode": "100019",
        "TotalPrizeValue": 100
      },
      {
        "MaxResult": 5,
        "CouponCode": "100026",
        "TotalPrizeValue": 0
      },
      {
        "MaxResult": 10,
        "CouponCode": "100033",
        "TotalPrizeValue": 961.6088
      },
      {
        "MaxResult": 5,
        "CouponCode": "100040",
        "TotalPrizeValue": 0
      },
      {
        "MaxResult": 6,
        "CouponCode": "100057",
        "TotalPrizeValue": 60
      },
      {
        "MaxResult": 9,
        "CouponCode": "100064",
        "TotalPrizeValue": 341.1707
      },
      {
        "MaxResult": 4,
        "CouponCode": "100071",
        "TotalPrizeValue": 0
      },
      {
        "MaxResult": 5,
        "CouponCode": "100088",
        "TotalPrizeValue": 0
      }
    ]
  }
}
"""

data = json.loads(json_str)

# SOURCE: https://ru.stackoverflow.com/questions/671333

df = pd.DataFrame(data["d"]["Items"])
df.set_index("CouponCode")["TotalPrizeValue"].reset_index().to_excel("result.xlsx")
