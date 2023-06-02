#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install peewee
from peewee import *


db = SqliteDatabase("games.sqlite", pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = db


class Game(BaseModel):
    name = CharField(unique=True)

    def get_genres(self) -> list["Genre"]:
        return [link.genre for link in self.links_to_genres]

    def append_genres(self, *genres: list["Genre"]):
        for genre in genres:
            GameToGenre.get_or_create(game=self, genre=genre)


class Genre(BaseModel):
    name = CharField(unique=True)
    description = TextField(null=True)

    def get_games(self) -> list[Game]:
        return [link.game for link in self.links_to_games]


class GameToGenre(BaseModel):
    game = ForeignKeyField(Game, backref="links_to_genres")
    genre = ForeignKeyField(Genre, backref="links_to_games")

    class Meta:
        indexes = (
            (("game", "genre"), True),
        )


db.connect()
db.create_tables([Game, Genre, GameToGenre])


# Initialization
GENRE__SURVIVAL_HORROR, _ = Genre.get_or_create(name="Survival horror")
GENRE__TPS, _ = Genre.get_or_create(name="TPS", description="Third-person shooter")
GENRE__RPG, _ = Genre.get_or_create(name="RPG", description="Role playing game")
GENRE__ACTION, _ = Genre.get_or_create(name="Action")
GENRE__ACTION_ADVENTURE, _ = Genre.get_or_create(name="Action-adventure")

if not Game.select().exists():
    game, _ = Game.get_or_create(name="Dead Space")
    game.append_genres(GENRE__SURVIVAL_HORROR, GENRE__TPS)

    game, _ = Game.get_or_create(name="Dead Island")
    game.append_genres(GENRE__SURVIVAL_HORROR, GENRE__RPG)

    game, _ = Game.get_or_create(name="Dying Light")
    game.append_genres(GENRE__SURVIVAL_HORROR, GENRE__ACTION, GENRE__RPG)

    game, _ = Game.get_or_create(name="Dark Souls")
    game.append_genres(GENRE__ACTION, GENRE__RPG)

    game, _ = Game.get_or_create(name="Darksiders III")
    game.append_genres(GENRE__ACTION, GENRE__RPG, GENRE__ACTION_ADVENTURE)


if __name__ == "__main__":
    print(f"Genre {GENRE__SURVIVAL_HORROR.name!r}:")
    for game in GENRE__SURVIVAL_HORROR.get_games():
        print(f"    {game.name}")
    # Genre 'Survival horror':
    #     Dead Space
    #     Dead Island
    #     Dying Light

    print("\n" + "-" * 10 + "\n")

    game, _ = Game.get_or_create(name="Dying Light")
    print(f"Game {game.name!r}:")
    for genre in game.get_genres():
        print(f"    {genre.name}: {genre.description!r}")
    # Game 'Dying Light':
    #     Survival horror: None
    #     RPG: 'Role playing game'
    #     Action: None

    print("\n" + "-" * 10 + "\n")

    for game in Game.select():
        print(
            f"{game.name}\n    Genres: {', '.join(genre.name for genre in game.get_genres())}"
        )
        print()

    # Dead Space
    #     Genres: Survival horror, TPS
    #
    # Dead Island
    #     Genres: Survival horror, RPG
    #
    # Dying Light
    #     Genres: Survival horror, RPG, Action
    #
    # Dark Souls
    #     Genres: RPG, Action
    #
    # Darksiders III
    #     Genres: RPG, Action, Action-adventure
