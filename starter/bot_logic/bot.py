import random
import numpy as np
import queue
from core.logging import log
from models.action import Action
from models.tile import Tile


def in_bound(position, state):
    return 0 <= position[0] < state.width and 0 <= position[1] < state.height


def get_position_in_direction(position, direction, distance=1):
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
    direction_vector = tuple(np.subtract(destination, origin))
    if direction_vector == (0, -1):
        return Action.UP
    elif direction_vector == (0, 1):
        return Action.DOWN
    elif direction_vector == (-1, 0):
        return Action.LEFT
    elif direction_vector == (1, 0):
        return Action.RIGHT
    elif direction_vector == (0, 0):
        return Action.STAY


def get_nbr_of_breakable_block(destination_to_explore, directions, bomb_range, state):
    broken_block = 0
    for direction in directions:
        for sight in range(1, bomb_range + 1):
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

    return broken_block


def get_closest_best_position_to_drop_a_bomb(score_matrix, distance_matrix, state):
    best_position_to_drop_a_bomb = None
    max_score = np.amax(score_matrix)
    shortest_path = np.amax(distance_matrix)
    for column in range(0, state.width):
        for line in range(0, state.height):
            if score_matrix[column, line] == max_score:
                if distance_matrix[column, line] < shortest_path:
                    shortest_path = distance_matrix[column, line]
                    best_position_to_drop_a_bomb = (column, line)
    return best_position_to_drop_a_bomb


def is_in_danger(bomb, directions, state, destination):
    for direction in directions:
        for sight in range(0, bomb.range + 1):
            bomb_target = get_position_in_direction(bomb.position, direction, sight)

            if in_bound(bomb_target, state):
                if state.tiles[bomb_target] == Tile.WALL:
                    break
                elif bomb_target == destination:
                    return True
            else:
                break
    return False


def get_closest_safe_position(current_location, directions, bombs, state):
    possible_safe_destinations = queue.Queue()
    possible_safe_destinations.put(current_location)
    distance_matrix = np.full((state.width, state.height), state.width * state.height)
    distance_matrix[current_location] = 0
    while not possible_safe_destinations.empty():
        safe = True
        possible_safe_destination = possible_safe_destinations.get()
        for bomb in bombs:
            if is_in_danger(bomb, directions, state, possible_safe_destination):
                safe = False
                for direction in directions:
                    next_possible_safe_destination = get_position_in_direction(possible_safe_destination, direction)

                    if in_bound(next_possible_safe_destination, state):
                        if state.tiles[next_possible_safe_destination] == Tile.EMPTY or state.tiles[next_possible_safe_destination] == Tile.EXPLOSION:
                            if distance_matrix[next_possible_safe_destination] > distance_matrix[possible_safe_destination] + 1:
                                distance_matrix[next_possible_safe_destination] = distance_matrix[possible_safe_destination] + 1
                                possible_safe_destinations.put(next_possible_safe_destination)

                break
        if safe:
            next_position_to_go = possible_safe_destination
            while distance_matrix[next_position_to_go] > 1:
                best_neighbor = next_position_to_go
                for direction in directions:
                    next_position_in_shortest_path = get_position_in_direction(next_position_to_go, direction)

                    if in_bound(next_position_in_shortest_path, state):
                        if distance_matrix[next_position_in_shortest_path] < distance_matrix[best_neighbor]:
                            best_neighbor = next_position_in_shortest_path

                next_position_to_go = best_neighbor
            return next_position_to_go
    log(distance_matrix.transpose())


def get_shortest_path(destination, distance_matrix, directions, state):
    shortest_path = [destination]
    next_position_to_go = destination
    while distance_matrix[next_position_to_go] > 1:
        best_neighbor = next_position_to_go
        for direction in directions:
            next_position_in_shortest_path = get_position_in_direction(next_position_to_go, direction)

            if in_bound(next_position_in_shortest_path, state):
                if distance_matrix[next_position_in_shortest_path] < distance_matrix[best_neighbor]:
                    best_neighbor = next_position_in_shortest_path
        next_position_to_go = best_neighbor

        shortest_path.insert(0, best_neighbor)

    return shortest_path


def get_score_and_distance_matrix(current_location, state, directions, my_bot):
    score_matrix = np.zeros((state.width, state.height))
    distance_matrix = np.full((state.width, state.height), state.width * state.height)
    possible_destinations = []
    destinations_to_explore = [current_location]
    distance_matrix[current_location] = 0

    while len(destinations_to_explore) > 0:
        destination_to_explore = destinations_to_explore.pop()

        for direction in directions:
            next_destination_to_explore = get_position_in_direction(destination_to_explore, direction)

            if in_bound(next_destination_to_explore, state):
                if state.tiles[next_destination_to_explore] == Tile.EMPTY or state.tiles[next_destination_to_explore] == Tile.EXPLOSION:
                    if next_destination_to_explore not in possible_destinations:
                        possible_destinations.append(next_destination_to_explore)

                    if distance_matrix[next_destination_to_explore] > distance_matrix[destination_to_explore] + 1:
                        destinations_to_explore.append(next_destination_to_explore)
                        distance_matrix[next_destination_to_explore] = distance_matrix[destination_to_explore] + 1

        score_matrix[destination_to_explore] = get_nbr_of_breakable_block(destination_to_explore, directions, my_bot.bomb_range, state)

    return score_matrix, distance_matrix, possible_destinations


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
        directions = [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]
        current_location = (my_bot.x, my_bot.y)

        score_matrix, distance_matrix, possible_destinations = get_score_and_distance_matrix(current_location, state, directions, my_bot)

        max_score = np.amax(score_matrix)
        if max_score == 0:
            best_position_to_drop_a_bomb = (state.width // 2, state.height // 2)
        else:
            best_position_to_drop_a_bomb = get_closest_best_position_to_drop_a_bomb(score_matrix, distance_matrix, state)

        shortest_path = get_shortest_path(best_position_to_drop_a_bomb, distance_matrix, directions, state)
        next_position_to_go = shortest_path[0]

        possible_destinations.sort()
        log(f"Tick: {state.tick};\n"
            f"Possible destinations: {possible_destinations};\n"
            f"Max Score: {max_score}\n"
            f"Best position to drop a bomb: {best_position_to_drop_a_bomb};\n"
            f"Max amount of breakable block: {np.max(score_matrix, axis=None)};\n"
            f"Min distance: {distance_matrix[best_position_to_drop_a_bomb]};\n"
            f"Current location: {current_location};\n"
            f"Next position to go to: {shortest_path};\n"
            f"{distance_matrix.transpose()}\n"
            f"{score_matrix.transpose()}"
            )

        action = get_direction_relative_to_position(current_location, next_position_to_go)

        for bomb in state.bombs:
            if is_in_danger(bomb, directions, state, next_position_to_go):
                log("I'M IN DANGER")
                next_position_to_go = get_closest_safe_position(current_location, directions, state.bombs, state)
                log(next_position_to_go)
                if next_position_to_go:
                    action = get_direction_relative_to_position(current_location, next_position_to_go)
                else:
                    break

        if action == Action.STAY and current_location == best_position_to_drop_a_bomb:
            action = Action.BOMB
        return action
