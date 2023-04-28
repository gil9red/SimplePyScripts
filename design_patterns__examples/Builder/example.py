#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Builder — Строитель
# SOURCE: https://ru.wikipedia.org/wiki/Строитель_(шаблон_проектирования)


from abc import ABC, abstractmethod


# "Product"
class Pizza:
    def __init__(self):
        self._dough = ""
        self._sauce = ""
        self._topping = ""

    def set_dough(self, dough: str):
        self._dough = dough

    def set_sauce(self, sauce: str):
        self._sauce = sauce

    def set_topping(self, topping: str):
        self._topping = topping

    def __str__(self):
        return f'Pizza(dough="{self._dough}, sauce="{self._sauce}, topping="{self._topping}")'


# "Abstract Builder"
class PizzaBuilder(ABC):
    def __init__(self):
        self._pizza = None

    def get_pizza(self) -> Pizza:
        return self._pizza

    def create_new_pizza_product(self):
        self._pizza = Pizza()

    @abstractmethod
    def build_dough(self):
        pass

    @abstractmethod
    def build_sauce(self):
        pass

    @abstractmethod
    def build_topping(self):
        pass


# "ConcreteBuilder"
class HawaiianPizzaBuilder(PizzaBuilder):
    def build_dough(self):
        self._pizza.set_dough("cross")

    def build_sauce(self):
        self._pizza.set_sauce("mild")

    def build_topping(self):
        self._pizza.set_topping("ham+pineapple")


# "ConcreteBuilder"
class SpicyPizzaBuilder(PizzaBuilder):
    def build_dough(self):
        self._pizza.set_dough("pan baked")

    def build_sauce(self):
        self._pizza.set_sauce("hot")

    def build_topping(self):
        self._pizza.set_topping("pepperoni+salami")


# "Director"
class Waiter:
    def __init__(self):
        self.pizza_builder = None

    def set_pizza_builder(self, pb: PizzaBuilder):
        self.pizza_builder = pb

    def get_pizza(self) -> Pizza:
        return self.pizza_builder.get_pizza()

    def construct_pizza(self):
        self.pizza_builder.create_new_pizza_product()
        self.pizza_builder.build_dough()
        self.pizza_builder.build_sauce()
        self.pizza_builder.build_topping()


if __name__ == "__main__":
    # A customer ordering a pizza.
    hawaiianPizzaBuilder = HawaiianPizzaBuilder()

    waiter = Waiter()
    waiter.set_pizza_builder(hawaiianPizzaBuilder)
    waiter.construct_pizza()

    pizza = waiter.get_pizza()
    print(pizza)
