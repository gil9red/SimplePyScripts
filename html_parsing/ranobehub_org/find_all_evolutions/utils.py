#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TreeNode:
    name: str
    is_last: bool = False
    parent: 'TreeNode' = field(default=None, repr=False)
    children: list['TreeNode'] = field(default_factory=list, init=False, repr=False)

    def is_finished(self) -> bool:
        if self.is_last:
            return True

        if not self.children:
            return False

        return all(node.is_finished() for node in self.children)

    def add_child(self, name: str, is_last: bool = False) -> 'TreeNode':
        if node := self.get_child([name]):
            return node

        if self.is_last:
            raise Exception("Нельзя добавить дочерний узел в последний узел")

        node = TreeNode(name=name, is_last=is_last, parent=self)
        self.children.append(node)
        return node

    def get_child(self, names: list[str], children: list['TreeNode'] = None) -> Optional['TreeNode']:
        if children is None:
            children = self.children

        name = names[0]
        for node in children:
            if node.name == name:
                if len(names) == 1:
                    return node

                return self.get_child(names[1:], node.children)

    def get_full_name(self, sep: str = " >> ") -> str:
        names: list[str] = [self.name]

        parent = self.parent
        while parent and parent.name:
            names.append(parent.name)
            parent = parent.parent

        names.reverse()
        return sep.join(names)

    def print(self):
        # Проверка на корневой узел
        if self.name:
            print(self.get_full_name())

        for child in self.children:
            child.print()


@dataclass
class Tree:
    root_node: TreeNode = TreeNode(name="")

    def add_child(self, name: str, is_last: bool = False) -> TreeNode:
        return self.root_node.add_child(name=name, is_last=is_last)

    def get_child(self, names: list[str]) -> TreeNode | None:
        return self.root_node.get_child(names=names)

    def print(self):
        self.root_node.print()


def get_path_of_classes(path: str) -> list[str]:
    return [x.strip()[1:-1] for x in path.split("->")]



if __name__ == "__main__":
    path_of_classes = "[🗡️ Воин]->[⚔️ Рыцарь]->[🛡️Феодал]->[👑 Король]"
    assert get_path_of_classes(path_of_classes) == ["🗡️ Воин", "⚔️ Рыцарь", "🛡️Феодал", "👑 Король"]

    assert get_path_of_classes("[🗡️ Воин]") == ["🗡️ Воин"]

    tree = Tree()

    node_1 = tree.add_child("Воин")
    assert node_1 == tree.add_child("Воин")
    assert node_1.get_full_name() == "Воин"
    assert not node_1.is_finished()

    node_1_1 = node_1.add_child("Рыцарь")
    assert node_1_1 == node_1.add_child("Рыцарь")
    assert node_1_1.get_full_name() == "Воин >> Рыцарь"
    assert not node_1_1.is_finished()

    node_1_1_1 = node_1_1.add_child("Феодал")
    assert not node_1_1_1.is_finished()

    node_1_1_1_1 = node_1_1_1.add_child("Король", is_last=True)
    assert node_1_1_1_1.get_full_name() == "Воин >> Рыцарь >> Феодал >> Король"
    assert node_1.is_finished()
    assert node_1_1.is_finished()
    assert node_1_1_1.is_finished()
    assert node_1_1_1_1.is_finished()

    assert node_1 == tree.get_child(["Воин"])
    assert node_1_1_1 == tree.get_child(["Воин", "Рыцарь", "Феодал"])
    assert node_1_1_1_1 == tree.get_child(["Воин", "Рыцарь", "Феодал", "Король"])
    assert tree.get_child(["Воин", "Король"]) is None

    node_1_2 = node_1.add_child("Наемник")
    assert not node_1.is_finished()
    assert not node_1_2.is_finished()

    node_1_2_1 = node_1_2.add_child("Авантюрист")
    node_1_2_1_1 = node_1_2_1.add_child("Глава гильдии", is_last=True)
    assert node_1.is_finished()
    assert node_1_2_1_1.is_finished()

    node_1_2_2 = node_1_2.add_child("Разбойник")
    node_1_2_2_1 = node_1_2_2.add_child("Феодал", is_last=True)

    node_1_2_3 = node_1_2.add_child("Следопыт")

    node_2 = tree.add_child("Юный даос")

    node_2_1 = node_2.add_child("Школа зебры")
    node_2_1_1 = node_2_1.add_child("Духовный владыка")
    node_2_1_1_1 = node_2_1_1.add_child("Верховный даос", is_last=True)
    assert node_2_1_1_1.get_full_name() == "Юный даос >> Школа зебры >> Духовный владыка >> Верховный даос"

    node_2_2 = node_2.add_child("Школа тигра")
    node_2_2_1 = node_2_2.add_child("Скала")
    node_2_2_1_1 = node_2_2_1.add_child("Высший культиватор", is_last=True)
    assert node_2_2_1_1.get_full_name() == "Юный даос >> Школа тигра >> Скала >> Высший культиватор"

    tree.print()
    """
    Воин
    Воин >> Рыцарь
    Воин >> Рыцарь >> Феодал
    Воин >> Рыцарь >> Феодал >> Король
    Воин >> Наемник
    Воин >> Наемник >> Авантюрист
    Воин >> Наемник >> Авантюрист >> Глава гильдии
    Воин >> Наемник >> Разбойник
    Воин >> Наемник >> Разбойник >> Феодал
    Воин >> Наемник >> Следопыт
    Юный даос
    Юный даос >> Школа зебры
    Юный даос >> Школа зебры >> Духовный владыка
    Юный даос >> Школа зебры >> Духовный владыка >> Верховный даос
    Юный даос >> Школа тигра
    Юный даос >> Школа тигра >> Скала
    Юный даос >> Школа тигра >> Скала >> Высший культиватор
    """
