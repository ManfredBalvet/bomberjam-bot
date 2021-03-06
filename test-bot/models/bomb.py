from core.json_serializable import JSONSerializable


class Bomb(JSONSerializable):
    def __init__(self, bomb_json):
        self.countdown = bomb_json["countdown"]
        self.player_id = bomb_json["playerId"]
        self.range = bomb_json["range"]
        self.x = bomb_json["x"]
        self.y = bomb_json["y"]