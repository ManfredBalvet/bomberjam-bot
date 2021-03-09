import random
import numpy as np
from core.logging import log
from models.action import Action
from models.tile import Tile


def in_bound(position, state):
    return 0 <= position[0] < state.width and 0 <= position[1] < state.height


def get_position_in_direction(position, direction, distance):
    (x, y) = position
    if direction == Action.UP:
        return x, y - distance
    elif direction == Action.DOWN:
        return x, y + distance
    elif direction == Action.LEFT:
        return x - distance, y
    elif direction == Action.RIGHT:
        return x + distance, y


def get_direction_relative_to_position(origin, destination):
    if tuple(np.subtract(destination, origin)) == (0, -1):
        return Action.UP
    elif tuple(np.subtract(destination, origin)) == (0, 1):
        return Action.DOWN
    elif tuple(np.subtract(destination, origin)) == (-1, 0):
        return Action.LEFT
    elif tuple(np.subtract(destination, origin)) == (1, 0):
        return Action.RIGHT
    elif tuple(np.subtract(destination, origin)) == (0, 0):
        return Action.STAY


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
        destinations_to_explore = [current_location]
        distance_matrix[current_location] = 0

        while len(destinations_to_explore) > 0:
            destination_to_explore = destinations_to_explore.pop()
            broken_block = 0
            for direction in directions:
                for sight in range(1, my_bot.bomb_range + 1):
                    bomb_target = get_position_in_direction(destination_to_explore, direction, sight)

                    if in_bound(bomb_target, state):
                        if state.tiles[bomb_target] == Tile.EMPTY or state.tiles[bomb_target] == Tile.EXPLOSION:
                            continue
                        elif state.tiles[bomb_target] == Tile.BLOCK:
                            broken_block += 1
                            break
                        else:
                            break
                    else:
                        break

            for direction in directions:
                next_destination_to_explore = get_position_in_direction(destination_to_explore, direction, 1)

                if in_bound(next_destination_to_explore, state):
                    if state.tiles[next_destination_to_explore] == Tile.EMPTY or state.tiles[next_destination_to_explore] == Tile.EXPLOSION:
                        if next_destination_to_explore not in possible_destinations:
                            possible_destinations.append(next_destination_to_explore)

                        if distance_matrix[next_destination_to_explore] > distance_matrix[destination_to_explore] + 1:
                            destinations_to_explore.append(next_destination_to_explore)
                            distance_matrix[next_destination_to_explore] = distance_matrix[destination_to_explore] + 1

            score_matrix[destination_to_explore] = broken_block

        max_score = np.amax(score_matrix)
        shortest_path = np.amax(distance_matrix)
        best_position_to_drop_a_bomb = None
        if max_score == 0:
            best_position_to_drop_a_bomb = (state.width // 2, state.height // 2)
        else:
            for column in range(0, state.width):
                for line in range(0, state.height):
                    if score_matrix[column, line] == max_score:
                        if distance_matrix[column, line] < shortest_path:
                            shortest_path = distance_matrix[column, line]
                            best_position_to_drop_a_bomb = (column, line)

        minimum_distance = distance_matrix[best_position_to_drop_a_bomb]

        next_position_to_go = best_position_to_drop_a_bomb
        while distance_matrix[next_position_to_go] > 1:
            best_neighbor = next_position_to_go
            for direction in directions:
                next_position_in_shortest_path = get_position_in_direction(next_position_to_go, direction, 1)

                if in_bound(next_position_in_shortest_path, state):
                    if distance_matrix[next_position_in_shortest_path] < distance_matrix[best_neighbor]:
                        best_neighbor = next_position_in_shortest_path

            next_position_to_go = best_neighbor

        possible_destinations.sort()
        log(f"Tick: {state.tick};\n"
            f"Possible destinations: {possible_destinations};\n"
            f"Best position to drop a bomb: {best_position_to_drop_a_bomb};\n"
            f"Max amount of breakable block: {np.max(score_matrix, axis=None)};\n"
            f"Min distance: {minimum_distance};\n"
            f"Current location: {current_location};\n"
            f"Next position to go to: {next_position_to_go};\n"
            f"{distance_matrix.transpose()}\n"
            f"{score_matrix.transpose()}"
            )

        action = get_direction_relative_to_position(current_location, next_position_to_go)
        if action == Action.STAY and max_score != 0:
            return Action.BOMB

        return action
