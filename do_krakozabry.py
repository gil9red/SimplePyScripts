#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


encoding_1 = "utf-8"
encoding_2 = "cp1251"

text = "Ну и правильно, что обращаешься за помощью на стековерфлоу"

# РќСѓ Рё РїСЂР°РІРёР»СЊРЅРѕ, С‡С‚Рѕ РѕР±СЂР°С‰Р°РµС€СЊСЃСЏ Р·Р° РїРѕРјРѕС‰СЊСЋ РЅР° СЃС‚РµРєРѕРІРµСЂС„Р»РѕСѓ
print(text.encode(encoding_1).decode(encoding_2))
print(text)
#
# text = 'Р”РѕР±Р°РІСЊ Рє РІРѕРїСЂРѕСЃСѓ С‚РµРіРё'
# print(text.encode(encoding_2).decode(encoding_1))
