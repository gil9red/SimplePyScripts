#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Facade — Фасад
# SOURCE: https://ru.wikipedia.org/wiki/Фасад_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/facade


from abc import ABC


# Абстрактный музыкант - не является обязательной составляющей паттерна, введен для упрощения кода
class Musician(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    def output(self, text: str) -> None:
        print(self.name + " " + text + ".")


# Конкретные музыканты
class Vocalist(Musician):
    def sing_couplet(self, couplet_number: int) -> None:
        self.output("спел куплет №" + str(couplet_number))

    def sing_chorus(self) -> None:
        self.output("спел припев")


class Guitarist(Musician):
    def play_cool_opening(self) -> None:
        self.output("начинает с крутого вступления")

    def play_cool_riffs(self) -> None:
        self.output("играет крутые риффы")

    def play_another_cool_riffs(self) -> None:
        self.output("играет другие крутые риффы")

    def play_incredibly_cool_solo(self) -> None:
        self.output("выдает невероятно крутое соло")

    def play_final_accord(self) -> None:
        self.output("заканчивает песню мощным аккордом")


class Bassist(Musician):
    def follow_the_drums(self) -> None:
        self.output("следует за барабанами")

    def change_rhythm(self, type_rhythm: str) -> None:
        self.output("перешел на ритм " + type_rhythm + "a")

    def stop_playing(self) -> None:
        self.output("заканчивает играть")


class Drummer(Musician):
    def start_playing(self) -> None:
        self.output("начинает играть")

    def stop_playing(self) -> None:
        self.output("заканчивает играть")


# Фасад, в данном случае - знаменитая рок-группа
class BlackSabbath:
    def __init__(self) -> None:
        self.vocalist = Vocalist("Оззи Осборн")
        self.guitarist = Guitarist("Тони Айомми")
        self.bassist = Bassist("Гизер Батлер")
        self.drummer = Drummer("Билл Уорд")

    def play_cool_song(self) -> None:
        self.guitarist.play_cool_opening()
        self.drummer.start_playing()
        self.bassist.follow_the_drums()
        self.guitarist.play_cool_riffs()
        self.vocalist.sing_couplet(1)
        self.bassist.change_rhythm("припев")
        self.guitarist.play_another_cool_riffs()
        self.vocalist.sing_chorus()
        self.bassist.change_rhythm("куплет")
        self.guitarist.play_cool_riffs()
        self.vocalist.sing_couplet(2)
        self.bassist.change_rhythm("припев")
        self.guitarist.play_another_cool_riffs()
        self.vocalist.sing_chorus()
        self.bassist.change_rhythm("куплет")
        self.guitarist.play_incredibly_cool_solo()
        self.guitarist.play_cool_riffs()
        self.vocalist.sing_couplet(3)
        self.bassist.change_rhythm("припев")
        self.guitarist.play_another_cool_riffs()
        self.vocalist.sing_chorus()
        self.bassist.change_rhythm("куплет")
        self.guitarist.play_cool_riffs()
        self.bassist.stop_playing()
        self.drummer.stop_playing()
        self.guitarist.play_final_accord()


if __name__ == "__main__":
    print("OUTPUT:")
    band = BlackSabbath()
    band.play_cool_song()

    # OUTPUT:
    # Тони Айомми начинает с крутого вступления.
    # Билл Уорд начинает играть.
    # Гизер Батлер следует за барабанами.
    # Тони Айомми играет крутые риффы.
    # Оззи Осборн спел куплет №1.
    # Гизер Батлер перешел на ритм припевa.
    # Тони Айомми играет другие крутые риффы.
    # Оззи Осборн спел припев.
    # Гизер Батлер перешел на ритм куплетa.
    # Тони Айомми играет крутые риффы.
    # Оззи Осборн спел куплет №2.
    # Гизер Батлер перешел на ритм припевa.
    # Тони Айомми играет другие крутые риффы.
    # Оззи Осборн спел припев.
    # Гизер Батлер перешел на ритм куплетa.
    # Тони Айомми выдает невероятно крутое соло.
    # Тони Айомми играет крутые риффы.
    # Оззи Осборн спел куплет №3.
    # Гизер Батлер перешел на ритм припевa.
    # Тони Айомми играет другие крутые риффы.
    # Оззи Осборн спел припев.
    # Гизер Батлер перешел на ритм куплетa.
    # Тони Айомми играет крутые риффы.
    # Гизер Батлер заканчивает играть.
    # Билл Уорд заканчивает играть.
    # Тони Айомми заканчивает песню мощным аккордом.
