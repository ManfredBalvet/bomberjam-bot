import json
import numpy as np

from core.json_serializable import JSONSerializable
from models.player import Player
from models.bomb import Bomb
from models.bonus import Bonus


class State(JSONSerializable):
    def __init__(self, state_string, bot_id):
        json_state = json.loads(state_string)

        self.tick = json_state["tick"]
        self.is_finished = json_state["isFinished"]
        self.players = {player_id: Player(player_json) for player_id, player_json in json_state["players"].items()}
        self.bombs = {bomb_id: Bomb(bomb_json) for bomb_id, bomb_json in json_state["bombs"].items()}
        self.bonuses = {bonus_id: Bonus(bonus_json) for bonus_id, bonus_json in json_state["bonuses"].items()}
        self.width = json_state["width"]
        self.height = json_state["height"]
        self.sudden_death_countdown = json_state["suddenDeathCountdown"]
        self.is_sudden_death_enabled = json_state["isSuddenDeathEnabled"]

        self.my_bot = self.players[bot_id]

        # TODO This breaks JSONSerializable, probably due to it being a numpy array
        self.tiles = np.array(list(json_state["tiles"])).reshape((self.height, self.width)).transpose()
