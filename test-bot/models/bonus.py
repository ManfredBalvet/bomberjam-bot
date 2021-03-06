from core.enumerable_enum import EnumerableEnum
from core.json_serializable import JSONSerializable


class Bonus(JSONSerializable):
    def __init__(self, bonus_json):
        self.kind = bonus_json["kind"]
        self.x = bonus_json["x"]
        self.y = bonus_json["y"]


class BonusKind(EnumerableEnum):
    BOMB_COUNT = "bomb"
    BOMB_RANGE = "fire"
