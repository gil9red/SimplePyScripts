#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Facade — Фасад
# SOURCE: https://ru.wikipedia.org/wiki/Фасад_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/facade


# Реализации отдельных частей компьютера.
# У каждого метода классов имеется какая-то реализация, в данном примере она опущена.


# Class CPU, отвечает за работу процессора
class CPU:
    def freeze(self) -> None:
        pass

    def jump(self, position: int) -> None:
        pass

    def execute(self) -> None:
        pass


# Class Memory, отвечает за работу памяти
class Memory:
    BOOT_ADDRESS = 0x0005

    def load(self, position: int, data: bytes) -> None:
        pass


# Class HardDrive, отвечает за работу жёсткого диска
class HardDrive:
    BOOT_SECTOR = 0x001
    SECTOR_SIZE = 64

    def read(self, lba: int, size: int) -> bytes:
        pass


# Пример шаблона "Фасад"
# В качестве унифицированного объекта выступает Компьютер.
# За этим объектом будут скрыты, все детали работы его внутренних частей.
class Computer:
    def __init__(self) -> None:
        self._cpu = CPU()
        self._memory = Memory()
        self._hard_drive = HardDrive()

    # Упрощённая обработка поведения "запуск компьютера"
    def start_computer(self) -> None:
        self._cpu.freeze()
        self._memory.load(
            self._memory.BOOT_ADDRESS,
            self._hard_drive.read(
                self._hard_drive.BOOT_SECTOR, self._hard_drive.SECTOR_SIZE
            ),
        )
        self._cpu.jump(self._memory.BOOT_ADDRESS)
        self._cpu.execute()


if __name__ == "__main__":
    # Пользователям компьютера предоставляется Фасад (компьютер),
    # который скрывает все сложность работы с отдельными компонентами.
    computer = Computer()
    computer.start_computer()
