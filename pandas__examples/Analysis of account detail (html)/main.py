#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# TODO: сделать детализацию счета и заказать в html/excel
#       замаскировать телефоны
#       сделать обработку excel на pandas: Analysis of account detail (excel)

import zipfile
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup


with zipfile.ZipFile("Doc_df7c89c378c04e8daf69257ea95d9a2e.zip") as f:
    data_file = f.read("Doc_df7c89c378c04e8daf69257ea95d9a2e.html")

root = BeautifulSoup(data_file, "lxml")

records = []
for tr in root.select("table > tbody > tr"):
    td_list = tr.select("td")
    record = [
        td_list[1].text,  # 'Дата'
        td_list[2].text,  # 'Время'
        td_list[3].text,  # 'GMT'
        td_list[4].text,  # 'Номер'
        # td_list[5].text,  # 'Зона вызова'
        # td_list[6].text,  # 'Зона направления вызова/номер сессии'
        td_list[7].text,  # 'Услуга'
        td_list[9].text,  # 'Длительность/Объем (мин.:сек.)/(Kb)'
        float(td_list[10].text.replace(",", ".")),  # 'Стоимость руб. без НДС'
    ]
    records.append(record)

columns = [
    "Дата",
    "Время",
    "GMT",
    "Номер",
    # 'Зона вызова', 'Зона направления вызова/номер сессии',
    "Услуга",
    "Длительность/Объем (мин.:сек.)/(Kb)",
    "Стоимость руб. без НДС",
]


df = pd.DataFrame(data=records, columns=columns)
# print(df)
print("Total rows:", len(df))

df_with_null_price = df[df["Стоимость руб. без НДС"] == 0]
print("With null price:", len(df_with_null_price))

df_with_price = df[df["Стоимость руб. без НДС"] > 0]
print("With price:", len(df_with_price))

phone_list = sorted(set(df["Номер"].tolist()))
print(f"\nPhones ({len(phone_list)}): {phone_list}")

print("\nShow target phone:")
df_dns_shop = df[df["Номер"].str.contains("sms:DNS-SHOP")]
print(
    f"  DNS-SHOP: number: {len(df_dns_shop)}, total price: {df_dns_shop['Стоимость руб. без НДС'].sum()}"
)

df_maginfo = df[df["Номер"].str.contains("sms:Maginfo")]
print(
    f"  Maginfo: number: {len(df_maginfo)}, total price: {df_maginfo['Стоимость руб. без НДС'].sum()}"
)

df_sms_ru = df[df["Номер"].str.contains("sms:SMS.RU")]
print(
    f"  SMS.RU: number: {len(df_sms_ru)}, total price: {df_sms_ru['Стоимость руб. без НДС'].sum()}"
)

print("\nPrint details (Maginfo):")
print(df_maginfo.to_string())

# Посчитать сумму за июнь, июль и август
print("\nPrice for months 06, 07 and 08:")
print("  " + str(df[df["Дата"].str.contains(".06.")]["Стоимость руб. без НДС"].sum()))
print("  " + str(df[df["Дата"].str.contains(".07.")]["Стоимость руб. без НДС"].sum()))
print("  " + str(df[df["Дата"].str.contains(".08.")]["Стоимость руб. без НДС"].sum()))

print("\nPrint details sorting by price (top 10):")
df_with_price_sorted = df_with_price.sort_values(
    by="Стоимость руб. без НДС", ascending=True
).tail(10)
print(df_with_price_sorted.to_string())

df_by_phone = df_with_price[df_with_price["Номер"].str.contains("79510000000")]
print("\nPrint total price by phone:", df_by_phone["Стоимость руб. без НДС"].sum())

df_months_06_07_08 = df_with_price[
    df_with_price["Дата"].str.contains("|".join([".06.", ".07.", ".08."]))
]
print(
    "\nTotal price for months 06, 07 and 08:",
    df_months_06_07_08["Стоимость руб. без НДС"].sum(),
)
print(df_months_06_07_08.to_string())

#
# TODO: интересно было бы полностью силами пандаса такое подсчитать, а после выбрать какие столбцы в итоговой таблице
#       показать.
#       Таблице нужно поле Итого
#
print("\n\nPrint internet info:")
df_internet = df[df["Номер"] == "internet.mts.ru"]

data_list = sorted(
    set(df_internet["Дата"].tolist()),
    key=lambda data: datetime.strptime(data, "%d.%m.%Y"),
)

total_mb = 0

for data in data_list:
    kb_list = df_internet[df_internet["Дата"] == data][
        "Длительность/Объем (мин.:сек.)/(Kb)"
    ].tolist()
    kb_list = [int(kb.replace("Kb", "")) for kb in kb_list]
    sum_mb = sum(kb_list) // 1024
    total_mb += sum_mb

    print(data, sum_mb, "MB")

print("Total:", total_mb, "MB")
