#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import requests
from bs4 import BeautifulSoup


URL = 'https://www.vbr.ru/banki/kurs-valut/prodaja-usd/'


rs = requests.get(URL)
root = BeautifulSoup(rs.content, 'html.parser')

items = []
for tr in root.select('#bank_table > .show-detail'):
    tds = tr.select('td')
    td_name, _, td_buy, td_sell = tds

    name = td_name.get_text(strip=True)
    buy = td_buy.select_one('.currency-price').get_text(strip=True)
    sell = td_sell.select_one('.currency-price').get_text(strip=True)

    items.append((name, buy, sell))

print(f'Items ({len(items)}):')
for i, (name, buy, sell) in enumerate(items, 1):
    print(f'  {i:2}. {name!r}, buy={buy}, sell={sell}')

# Items (20):
#    1. 'Банк «Веста»', buy=76,10, sell=76,62
#    2. 'Банк «Спутник»', buy=75,00, sell=77,00
#    3. 'Всероссийский Банк Развития Регионов', buy=73,88, sell=76,13
#    4. 'Муниципальный Камчатпрофитбанк', buy=73,85, sell=74,60
#    5. 'Нокссбанк', buy=73,80, sell=75,60
#    6. 'Банк «Соколовский»', buy=73,75, sell=74,85
#    7. 'Плюс Банк', buy=73,70, sell=74,00
#    8. 'Банк «Москва-Сити»', buy=73,70, sell=75,00
#    9. 'Банк «Химик»', buy=73,70, sell=74,25
#   10. 'БайкалИнвестБанк', buy=73,67, sell=73,95
#   11. 'Кубаньторгбанк', buy=73,62, sell=74,44
#   12. 'Заубер Банк', buy=73,61, sell=74,09
#   13. 'Кошелев-Банк', buy=73,60, sell=74,10
#   14. 'Банк Казани', buy=73,55, sell=73,99
#   15. 'Тимер Банк', buy=73,54, sell=74,09
#   16. 'Банк «Агророс»', buy=73,51, sell=74,08
#   17. 'Владбизнесбанк', buy=73,50, sell=74,15
#   18. 'Банк «Новый век»', buy=73,50, sell=74,04
#   19. 'ПромТрансБанк', buy=73,50, sell=74,50
#   20. 'Трансстройбанк', buy=73,50, sell=74,10
