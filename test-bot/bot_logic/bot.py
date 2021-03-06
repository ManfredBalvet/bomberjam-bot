# Implement your bot logic here
# If you remove get_bot_name or get_action, make sure to update MyBot.py
# Otherwise, you can add anything you'd like
# ==============================================================================

import random
from core.logging import log
from models.action import Action


def get_bot_name():
    return "Guid"


def get_action(state):
    log(state)
    my_bot = state.my_bot
    log(state.tiles[my_bot.x, my_bot.y])

    return random.choice(Action.tolist())
