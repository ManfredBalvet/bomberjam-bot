import random
import numpy as np
from core.logging import log
from models.action import Action
from models.tile import Tile


class Bot:
    """
    Your Bomberjam bot.
    NAME and compute_next_action(state) are required and used by the game loop.
    The rest is up to you!
    """
    NAME = f"Manou{random.randint(0, 10000)}"

    def __init__(self, bot_id):
        self.bot_id = bot_id

    def compute_next_action(self, state):
        """
        Computes the next action your bot should do based on the current game state.

        :param state: The current game state
        :return: Action
        """

        my_bot = state.my_bot

        score_matrix = np.zeros((state.width, state.height))
        distance_matrix = np.full((state.width, state.height), state.width * state.height)
        directions = [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
        possible_destinations = []
        current_location = (my_bot.x, my_bot.y)
        destination_to_explore = [current_location]
        distance_matrix[current_location] = 0

        while len(destination_to_explore) > 0:
            (x, y) = destination_to_explore.pop()
            broken_block = 0
            for direction in directions:
                for sight in range(1, my_bot.bomb_range + 1):
                    target = None
                    if direction == Action.UP:
                        target = (x, y - sight)
                    elif direction == Action.DOWN:
                        target = (x, y + sight)
                    elif direction == Action.LEFT:
                        target = (x - sight, y)
                    elif direction == Action.RIGHT:
                        target = (x + sight, y)

                    if 0 <= target[0] < state.width and 0 <= target[1] < state.height:
                        if state.tiles[target] == Tile.EMPTY or state.tiles[target] == Tile.EXPLOSION:
                            continue
                        elif state.tiles[target] == Tile.BLOCK:
                            broken_block += 1
                            break
                        else:
                            break
                    else:
                        break

            for direction in directions:
                destination = None
                if direction == Action.UP:
                    destination = (x, y - 1)
                elif direction == Action.DOWN:
                    destination = (x, y + 1)
                elif direction == Action.LEFT:
                    destination = (x - 1, y)
                elif direction == Action.RIGHT:
                    destination = (x + 1, y)

                if 0 <= destination[0] < state.width and 0 <= destination[1] < state.height:
                    if state.tiles[destination] == Tile.EMPTY or state.tiles[destination] == Tile.EXPLOSION:
                        if destination not in possible_destinations:
                            possible_destinations.append(destination)
                        if distance_matrix[destination] > distance_matrix[x, y] + 1:
                            destination_to_explore.append(destination)
                            distance_matrix[destination] = distance_matrix[x, y] + 1

            score_matrix[x, y] = broken_block

        max_score = np.amax(score_matrix)
        shortest_path = np.amax(distance_matrix)
        best_destination = None
        for column in range(0, state.width):
            for line in range(0, state.height):
                if score_matrix[column, line] == max_score:
                    if distance_matrix[column, line] < shortest_path:
                        shortest_path = distance_matrix[column, line]
                        best_destination = (column, line)

        minimum_distance = distance_matrix[best_destination]

        position = best_destination
        while distance_matrix[position] > 1:
            (x, y) = position
            for direction in directions:
                destination = None
                if direction == Action.UP:
                    destination = (x, y - 1)
                elif direction == Action.DOWN:
                    destination = (x, y + 1)
                elif direction == Action.LEFT:
                    destination = (x - 1, y)
                elif direction == Action.RIGHT:
                    destination = (x + 1, y)

                if 0 <= destination[0] < state.width and 0 <= destination[1] < state.height:
                    if distance_matrix[destination] < distance_matrix[position]:
                        position = destination

        possible_destinations.sort()
        log(f"{possible_destinations};\n {best_destination}; {np.max(score_matrix, axis=None)}; {minimum_distance}")

        if max_score == 0:
            return Action.STAY
        elif tuple(np.subtract(position, current_location)) == (0, -1):
            return Action.UP
        elif tuple(np.subtract(position, current_location)) == (0, 1):
            return Action.DOWN
        elif tuple(np.subtract(position, current_location)) == (-1, 0):
            return Action.LEFT
        elif tuple(np.subtract(position, current_location)) == (1, 0):
            return Action.RIGHT
        elif tuple(np.subtract(position, current_location)) == (0, 0):
            return Action.BOMB
