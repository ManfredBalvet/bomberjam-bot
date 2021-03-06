from core.json_serializable import JSONSerializable


class Player(JSONSerializable):
    def __init__(self, player_json):
        self.id = player_json["id"]
        self.name = player_json["name"]
        self.x = player_json["x"]
        self.y = player_json["y"]
        self.starting_corner = player_json["startingCorner"]
        self.bombs_left = player_json["bombsLeft"]
        self.max_bombs = player_json["maxBombs"]
        self.bomb_range = player_json["bombRange"]
        self.is_alive = player_json["isAlive"]
        self.timed_out = player_json["timedOut"]
        self.respawning = player_json["respawning"]
        self.score = player_json["score"]
        self.color = player_json["color"]
