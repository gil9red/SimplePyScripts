#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Builder — Строитель


from typing import NamedTuple, List


class WokBase(NamedTuple):
    name: str
    description: str

    price: int
    weight: int

    class Factory:
        @staticmethod
        def create(name, description):
            return WokBase(name, description, price=129, weight=250)

        @staticmethod
        def create_small(name, description):
            return WokBase(name, description, price=89, weight=150)


class WokAdditive(NamedTuple):
    name: str
    price: int
    weight: int

    class Factory:
        @staticmethod
        def create(name, price):
            return WokAdditive(name, price, weight=50)

        @staticmethod
        def create_small(name, price):
            return WokAdditive(name, price, weight=30)


class WokSauce(NamedTuple):
    name: str
    price: int = 30
    weight: int = 50


class WokTopping(NamedTuple):
    name: str
    price: int = 10
    weight: int = 5


WokUdon = WokBase.Factory.create(
    name="Удон", description="Пшеничная лапша + свежие овощи"
)
WokUdonSmall = WokBase.Factory.create_small(
    name="Удон (эконом)", description="Пшеничная лапша + свежие овощи"
)

WokSoba = WokBase.Factory.create(
    name="Соба", description="Гречневая лапша + свежие овощи"
)
WokSobaSmall = WokBase.Factory.create_small(
    name="Соба (эконом)", description="Гречневая лапша + свежие овощи"
)

WokRamen = WokBase.Factory.create_small(
    name="Рамен", description="Яичная лапша + свежие овощи"
)
WokRamenSmall = WokBase.Factory.create_small(
    name="Рамен (эконом)", description="Яичная лапша + свежие овощи"
)

WokHarusame = WokBase.Factory.create(
    name="Харусаме", description="Рисовая лапша + свежие овощи"
)
WokHarusameSmall = WokBase.Factory.create_small(
    name="Харусаме (эконом)", description="Рисовая лапша + свежие овощи"
)

WokRice = WokBase.Factory.create(
    name="Рис", description="Цельнозерный рис + свежие овощи"
)
WokRiceSmall = WokBase.Factory.create_small(
    name="Рис (эконом)", description="Цельнозерный рис + свежие овощи"
)


WokAdditiveChicken = WokAdditive.Factory.create(name="Курица", price=58)
WokAdditiveChickenSmall = WokAdditive.Factory.create_small(
    name="Курица (эконом)", price=38
)

WokAdditiveBeef = WokAdditive.Factory.create(name="Говядина", price=84)
WokAdditiveBeefSmall = WokAdditive.Factory.create_small(
    name="Говядина (эконом)", price=64
)

WokAdditiveShrimp = WokAdditive.Factory.create(name="Креветка", price=109)
WokAdditiveShrimpSmall = WokAdditive.Factory.create_small(
    name="Креветка (эконом)", price=89
)

WokAdditiveSquid = WokAdditive.Factory.create(name="Кальмар", price=95)
WokAdditiveSquidSmall = WokAdditive.Factory.create_small(
    name="Кальмар (эконом)", price=75
)

WokAdditiveSeafood = WokAdditive.Factory.create(name="Морепродукты", price=94)
WokAdditiveSeafoodSmall = WokAdditive.Factory.create_small(
    name="Морепродукты (эконом)", price=74
)

WokAdditiveSalmon = WokAdditive.Factory.create(name="Лосось", price=102)
WokAdditiveSalmonSmall = WokAdditive.Factory.create_small(
    name="Лосось (эконом)", price=82
)

WokAdditiveShiitakeMushrooms = WokAdditive.Factory.create(
    name="Грибы Шиитаке", price=44
)
WokAdditiveShiitakeMushroomsSmall = WokAdditive.Factory.create_small(
    name="Грибы Шиитаке (эконом)", price=24
)


WokSauceCreamy = WokSauce(name="Сливочный соус")
WokSauceOyster = WokSauce(name="Устричный соус")
WokSauceCheese = WokSauce(name="Сырный соус")
WokSauceTeriyaki = WokSauce(name="Терияки соус")
WokSauceAcute = WokSauce(name="Острый соус")


WokToppingFriedOnions = WokTopping(name="Лук обжаренный")
WokToppingGreenOnion = WokTopping(name="Лук зеленый")
WokToppingRoastedSesame = WokTopping(name="Кунжут обжаренный")
WokToppingChilli = WokTopping(name="Перец чили")
WokToppingParmesanCheese = WokTopping(name="Сыр пармезан")


class Wok:
    base: WokBase = None
    additive: WokAdditive = None
    sauce: WokSauce = None
    sauce_additional: WokSauce = None
    topping: List[WokTopping] = None

    def __init__(self):
        self.topping = []

    def get_order_text(self) -> str:
        """Текст заказа"""

        text = "Заказ:\n"

        for item in self.get_order_items():
            text += f"  {item.name:25} : {item.price} рублей\n"

        text += "  {:25} : {} рублей".format("", self.get_order_price())

        return text

    def get_order_items(self) -> list:
        """Элементы заказа"""

        items = [self.base, self.additive, self.sauce]

        if self.sauce_additional:
            items.append(self.sauce_additional)

        items.extend(self.topping)

        return items

    def get_order_price(self) -> int:
        """Стоимость заказа"""

        return sum(x.price for x in self.get_order_items())

    def get_order_weight(self) -> int:
        """Примерный вес заказа"""

        return sum(x.weight for x in self.get_order_items())

    class Builder:
        def __init__(self):
            self.wok = Wok()

        def set_base(self, base: WokBase) -> "Builder":
            """Основа"""

            self.wok.base = base
            return self

        def set_additive(self, additive: WokAdditive) -> "Builder":
            """Добавка"""

            self.wok.additive = additive
            return self

        def set_sauce(self, sauce: WokSauce) -> "Builder":
            """Соус"""

            self.wok.sauce = sauce._replace(price=0)
            return self

        def set_sauce_additional(self, sauce: WokSauce) -> "Builder":
            """Дополнительный соус"""

            self.wok.sauce_additional = sauce
            return self

        def add_topping(self, topping: WokTopping) -> "Builder":
            """Топпинг"""

            self.wok.topping.append(topping)
            return self

        def build(self) -> "Wok":
            return self.wok


class WokDirector:
    @staticmethod
    def make_economy() -> Wok:
        return (
            Wok.Builder()
            .set_base(WokSoba)
            .set_additive(WokAdditiveChickenSmall)
            .set_sauce(WokSauceCheese)
            .build()
        )

    @staticmethod
    def make_business_lunch() -> Wok:
        return (
            Wok.Builder()
            .set_base(WokUdon)
            .set_additive(WokAdditiveChicken)
            .set_sauce(WokSauceCreamy)
            .build()
        )

    @staticmethod
    def make_vegetarian() -> Wok:
        return (
            Wok.Builder()
            .set_base(WokUdon)
            .set_additive(WokAdditiveShiitakeMushrooms)
            .set_sauce(WokSauceTeriyaki)
            .add_topping(WokToppingGreenOnion)
            .build()
        )


if __name__ == "__main__":
    wok = (
        Wok.Builder()
        .set_base(WokUdon)
        .set_additive(WokAdditiveBeef)
        .set_sauce(WokSauceCheese)
        .build()
    )
    print(wok.get_order_price())  # 213
    print(wok.get_order_weight())  # 350
    print(wok.get_order_text())
    # Заказ:
    #   Удон                      : 129 рублей
    #   Говядина                  : 84 рублей
    #   Сырный соус               : 0 рублей
    #                             : 213 рублей
    print()

    wok = (
        Wok.Builder()
        .set_base(WokSoba)
        .set_additive(WokAdditiveBeef)
        .set_sauce(WokSauceCheese)
        .add_topping(WokToppingFriedOnions)
        .add_topping(WokToppingGreenOnion)
        .add_topping(WokToppingChilli)
        .build()
    )
    print(wok.get_order_price())  # 243
    print(wok.get_order_weight())  # 365
    print(wok.get_order_text())
    # Заказ:
    #   Соба                      : 129 рублей
    #   Говядина                  : 84 рублей
    #   Сырный соус               : 0 рублей
    #   Лук обжаренный            : 10 рублей
    #   Лук зеленый               : 10 рублей
    #   Перец чили                : 10 рублей
    #                             : 243 рублей

    print("\n")

    print(WokDirector.make_economy().get_order_text())
    print(WokDirector.make_business_lunch().get_order_text())
    print(WokDirector.make_vegetarian().get_order_text())
