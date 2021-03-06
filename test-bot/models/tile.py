from core.enumerable_enum import EnumerableEnum


class Tile(EnumerableEnum):
    EMPTY = "."
    EXPLOSION = "*"
    BLOCK = "+"
    WALL = "#"
