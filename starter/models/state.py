import json
import numpy as np

from core.json_serializable import JSONSerializable
from models.player import Player
from models.bomb import Bomb
from models.bonus import Bonus


class State(JSONSerializable):
    """
    The complete game representation.

    Game Attributes:
        tiles: Represents the map in a numpy array. You can access any Tile with state.tiles[x, y]
        tick: The current game tick
        is_finished: whether or not the game is finished
        players: A dict with all players in the game. The keys are the player ids
        bombs: A dict with all bombs in the game. The keys are the bomb ids
        bonuses: A dict with all bonuses in the game. The keys are the bonus ids
        width: The width of the map
        height: The height of the map
        sudden_death_countdown: When the sudden death countdown reaches 0, the sudden death starts
        is_sudden_death_enabled: True when sudden death is active. During sudden death, respawning is disabled

    Utility Attributes
        my_bot: Represents the current player.
    """

    def __init__(self, state_string, current_player_id):
        """
        :param state_string: A json string representing the state
        :param current_player_id: The id of the current player
        """
        json_state = json.loads(state_string)

        self.tick = json_state["tick"]
        self.is_finished = json_state["isFinished"]
        self.players = {player_id: Player(player_json) for player_id, player_json in json_state["players"].items()}
        self.bombs = [Bomb(bomb_json) for _, bomb_json in json_state["bombs"].items()]
        self.bonuses = {bonus_id: Bonus(bonus_json) for bonus_id, bonus_json in json_state["bonuses"].items()}
        self.width = json_state["width"]
        self.height = json_state["height"]
        self.sudden_death_countdown = json_state["suddenDeathCountdown"]
        self.is_sudden_death_enabled = json_state["isSuddenDeathEnabled"]
        self.tiles = np.array(list(json_state["tiles"])).reshape((self.height, self.width)).transpose()

        self.my_bot = self.players[current_player_id]

    def __get_dict__(self):
        """
        A numpy array is not JSON serializable so we force it to a list

        :return: dict
        """
        dict_copy = self.__dict__.copy()
        dict_copy['tiles'] = dict_copy['tiles'].tolist()

        return dict_copy
