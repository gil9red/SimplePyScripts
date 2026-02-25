#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from utils import get_bosses, Boss


def print_bosses(bosses: dict[str, list[Boss]], only_names=False) -> None:
    total = sum(len(i) for i in bosses.values())
    print(f"Hollow Knight ({total}):")

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
    # ...

    print_bosses(bosses_by_category, only_names=True)
    """
    Hollow Knight (40):
        Боссы (33):
            1. "Матка Жужж"
            2. "Ложный Рыцарь/Сломленный чемпион"
            3. "Задумчивый чревень"
            4. "Закруглан"
            5. "Воин душ"
            6. "Король мстекрылов"
            7. "Разбитый Сосуд/Потерянный собрат"
            8. "Кристаллический страж"
            9. "Навозный защитник"
            10. "Тремоматка"
            11. "Божья укротительница"
            12. "Полый рыцарь"
            13. "Хорнет"
            14. "Лорды богомолов"
            15. "Носк"
            16. "Мастер душ/Душегуб"
            17. "Коллекционер"
            18. "Лучезарность"
            19. "Предавший лорд"
            20. "Ууму"
            21. "Рыцарь-хранитель"
            22. "Серый принц Зот"
            23. "Белый защитник"
            24. "Гримм"
            25. "Король кошмара"
            26. "Рыцарь Улья"
            27. "Мастера гвоздя Оро и Мато"
            28. "Мастер кисти Шео"
            29. "Великий гуру гвоздей Слай"
            30. "Боевые сёстры"
            31. "Крылатый Носк"
            32. "Чистый Сосуд"
            33. "Всевышняя Лучезарность"
    
        Воины грёз (7):
            1. "Старейшина Ху"
            2. "Гальен"
            3. "Горб"
            4. "Маркот"
            5. "Марму"
            6. "Незрячая"
            7. "Ксеро"
    """
