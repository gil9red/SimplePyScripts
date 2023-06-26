#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from utils import get_bosses, Boss


def print_bosses(bosses: dict[str, list[Boss]], only_names=False):
    total = sum(len(i) for i in bosses.values())
    print(f"Salt and Sanctuary ({total}):")

    for category, bosses in bosses.items():
        print(f"    {category} ({len(bosses)}):")

        for i, boss in enumerate(bosses, 1):
            if only_names:
                print(f'        {i}. "{boss.name}"')
            else:
                print(f'        {i}. "{boss.name}": {boss.url}')

        print()

    print()


if __name__ == "__main__":
    bosses_by_category = get_bosses()
    print_bosses(bosses_by_category)
    # Salt and Sanctuary (23):
    #     Обязательные боссы (12):
    #         1. "Обезумевший рыцарь": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9E%D0%B1%D0%B5%D0%B7%D1%83%D0%BC%D0%B5%D0%B2%D1%88%D0%B8%D0%B9_%D1%80%D1%8B%D1%86%D0%B0%D1%80%D1%8C
    #         2. "Краекан циклоп": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9A%D1%80%D0%B0%D0%B5%D0%BA%D0%B0%D0%BD_%D1%86%D0%B8%D0%BA%D0%BB%D0%BE%D0%BF
    #         3. "Безумный алхимик": https://saltandsanctuary.fandom.com/ru/wiki/%D0%91%D0%B5%D0%B7%D1%83%D0%BC%D0%BD%D1%8B%D0%B9_%D0%B0%D0%BB%D1%85%D0%B8%D0%BC%D0%B8%D0%BA
    #         4. "Фальшивый шут": https://saltandsanctuary.fandom.com/ru/wiki/%D0%A4%D0%B0%D0%BB%D1%8C%D1%88%D0%B8%D0%B2%D1%8B%D0%B9_%D1%88%D1%83%D1%82
    #         5. "Краекан вирм": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9A%D1%80%D0%B0%D0%B5%D0%BA%D0%B0%D0%BD_%D0%B2%D0%B8%D1%80%D0%BC
    #         6. "Нетронутый инквизитор": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9D%D0%B5%D1%82%D1%80%D0%BE%D0%BD%D1%83%D1%82%D1%8B%D0%B9_%D0%B8%D0%BD%D0%BA%D0%B2%D0%B8%D0%B7%D0%B8%D1%82%D0%BE%D1%80
    #         7. "Третий агнец": https://saltandsanctuary.fandom.com/ru/wiki/%D0%A2%D1%80%D0%B5%D1%82%D0%B8%D0%B9_%D0%B0%D0%B3%D0%BD%D0%B5%D1%86
    #         8. "Иссушенный король": https://saltandsanctuary.fandom.com/ru/wiki/%D0%98%D1%81%D1%81%D1%83%D1%88%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9_%D0%BA%D0%BE%D1%80%D0%BE%D0%BB%D1%8C
    #         9. "Ведьма озера": https://saltandsanctuary.fandom.com/ru/wiki/%D0%92%D0%B5%D0%B4%D1%8C%D0%BC%D0%B0_%D0%BE%D0%B7%D0%B5%D1%80%D0%B0
    #         10. "Бескожий и Архитектор": https://saltandsanctuary.fandom.com/ru/wiki/%D0%91%D0%B5%D1%81%D0%BA%D0%BE%D0%B6%D0%B8%D0%B9_%D0%B8_%D0%90%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D0%BE%D1%80
    #         11. "Краекан дракон Скоурж": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9A%D1%80%D0%B0%D0%B5%D0%BA%D0%B0%D0%BD_%D0%B4%D1%80%D0%B0%D0%BA%D0%BE%D0%BD_%D0%A1%D0%BA%D0%BE%D1%83%D1%80%D0%B6
    #         12. "Безымянный бог": https://saltandsanctuary.fandom.com/ru/wiki/%D0%91%D0%B5%D0%B7%D1%8B%D0%BC%D1%8F%D0%BD%D0%BD%D1%8B%D0%B9_%D0%B1%D0%BE%D0%B3
    #
    #     Опциональные боссы (11):
    #         1. "Немая бездна": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9D%D0%B5%D0%BC%D0%B0%D1%8F_%D0%B1%D0%B5%D0%B7%D0%B4%D0%BD%D0%B0
    #         2. "Королева улыбок": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9A%D0%BE%D1%80%D0%BE%D0%BB%D0%B5%D0%B2%D0%B0_%D1%83%D0%BB%D1%8B%D0%B1%D0%BE%D0%BA
    #         3. "Древо людей": https://saltandsanctuary.fandom.com/ru/wiki/%D0%94%D1%80%D0%B5%D0%B2%D0%BE_%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9
    #         4. "Выпотрошенная оболочка": https://saltandsanctuary.fandom.com/ru/wiki/%D0%92%D1%8B%D0%BF%D0%BE%D1%82%D1%80%D0%BE%D1%88%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F_%D0%BE%D0%B1%D0%BE%D0%BB%D0%BE%D1%87%D0%BA%D0%B0
    #         5. "Отвратительный смрад": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9E%D1%82%D0%B2%D1%80%D0%B0%D1%82%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D1%81%D0%BC%D1%80%D0%B0%D0%B4
    #         6. "Кран Ронин": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9A%D1%80%D0%B0%D0%BD_%D0%A0%D0%BE%D0%BD%D0%B8%D0%BD
    #         7. "Мёрдиела Мол": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9C%D1%91%D1%80%D0%B4%D0%B8%D0%B5%D0%BB%D0%B0_%D0%9C%D0%BE%D0%BB
    #         8. "Бескровный принц": https://saltandsanctuary.fandom.com/ru/wiki/%D0%91%D0%B5%D1%81%D0%BA%D1%80%D0%BE%D0%B2%D0%BD%D1%8B%D0%B9_%D0%BF%D1%80%D0%B8%D0%BD%D1%86
    #         9. "Жаждущий": https://saltandsanctuary.fandom.com/ru/wiki/%D0%96%D0%B0%D0%B6%D0%B4%D1%83%D1%89%D0%B8%D0%B9_(%D0%B1%D0%BE%D1%81%D1%81)
    #         10. "Карсджоу Жестокий": https://saltandsanctuary.fandom.com/ru/wiki/%D0%9A%D0%B0%D1%80%D1%81%D0%B4%D0%B6%D0%BE%D1%83_%D0%96%D0%B5%D1%81%D1%82%D0%BE%D0%BA%D0%B8%D0%B9
    #         11. "Забытый король": https://saltandsanctuary.fandom.com/ru/wiki/%D0%97%D0%B0%D0%B1%D1%8B%D1%82%D1%8B%D0%B9_%D0%BA%D0%BE%D1%80%D0%BE%D0%BB%D1%8C

    print_bosses(bosses_by_category, only_names=True)
    # Salt and Sanctuary (23):
    #     Обязательные боссы (12):
    #         1. "Обезумевший рыцарь"
    #         2. "Краекан циклоп"
    #         3. "Безумный алхимик"
    #         4. "Фальшивый шут"
    #         5. "Краекан вирм"
    #         6. "Нетронутый инквизитор"
    #         7. "Третий агнец"
    #         8. "Иссушенный король"
    #         9. "Ведьма озера"
    #         10. "Бескожий и Архитектор"
    #         11. "Краекан дракон Скоурж"
    #         12. "Безымянный бог"
    #
    #     Опциональные боссы (11):
    #         1. "Немая бездна"
    #         2. "Королева улыбок"
    #         3. "Древо людей"
    #         4. "Выпотрошенная оболочка"
    #         5. "Отвратительный смрад"
    #         6. "Кран Ронин"
    #         7. "Мёрдиела Мол"
    #         8. "Бескровный принц"
    #         9. "Жаждущий"
    #         10. "Карсджоу Жестокий"
    #         11. "Забытый король"
