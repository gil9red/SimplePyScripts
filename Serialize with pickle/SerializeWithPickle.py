__author__ = "ipetrash"

# Serialization / Сериализация

# Example of using pickle module
# https://docs.python.org/3.4/library/pickle.html
import pickle


data = {
    "foo": [1, 2, 3],
    "bar": ("Hello", "world!"),
    "baz": True,
    "fiz": {
        1: "first",
        6: "six",
        "seven": 7,
    },
}

## Simple example
# write the serialized data in the file
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# open and read from a file
with open("data.pkl", "rb") as f:
    data = pickle.load(f)  # stored in the variable
    print(data)

## Maybe add a few data
# write the serialized data in the file
with open("data_1.pkl", "wb") as f:
    pickle.dump([1, 1, 2, 3], f)
    pickle.dump("Man", f)
    pickle.dump((666,), f)

with open("data_1.pkl", "rb") as f:
    # Need to preserve the order of reading
    fi = pickle.load(f)
    tw = pickle.load(f)
    th = pickle.load(f)
    print(fi)  # [1, 1, 2, 3]
    print(tw)  # Man
    print(th)  # (666,)

## Serialization of custom classes
class Monster:
    """Monster class!"""

    def __init__(self, health, power, name, level) -> None:
        self.health = health
        self.power = power
        self.name = name
        self.level = level
        self.abilities = ["Eater"]

    def __str__(self) -> str:
        return (
            f"Name: '{self.name}' lv {self.level}, health: {self.health}, "
            f"power: {self.power}, abilities: {self.abilities}: {hex(id(self))}"
        )

    def say(self) -> None:
        print("I'm %s" % self.name)

zombi = Monster(name="Zombi", health=100, power=10, level=2)
zombi.abilities.append("Undead")
zombi.abilities.append("Insensitivity to pain")

goblin = Monster(name="Goblin", health=50, power=8, level=1)
ork = Monster(name="Ork", health=250, power=25, level=4)

print()
print(Monster)
print(zombi)
print(goblin)
print(ork)

# write the serialized data in the file
with open("monster.pkl", "wb") as f:
    pickle.dump(Monster, f)
    pickle.dump(zombi, f)
    pickle.dump(goblin, f)
    pickle.dump(ork, f)

with open("monster.pkl", "rb") as f:
    m = pickle.load(f)  # get Monster
    z = pickle.load(f)  # get Zombi
    g = pickle.load(f)  # get Goblin
    o = pickle.load(f)  # get Ork
    print()
    print(m)
    print(z)
    print(g)
    print(o)

# Serialize: object -> string
temp_1 = pickle.dumps(zombi)
print()
print(temp_1)

# Serialize: string ->object
temp_2 = pickle.loads(temp_1)  # create new object
print(temp_2)
temp_2.say()
