import random

from core.commands import ActionCommand
from core.commands import RegisterBotCommand
from core.logging import configure_logging
from core.logging import log
from models.action import Action
from models.state import State

BOT_NAME = "Guid"

RegisterBotCommand(BOT_NAME).send()
bot_id = input()

configure_logging(f"MyBot-{bot_id}")
log(f"Bot name is '{BOT_NAME}' with id '{bot_id}'")

while True:
    state = State(input(), bot_id)
    log(state)

    try:
        tick = state.tick
        my_bot = state.my_bot

        random_action = random.choice(Action.all())
        ActionCommand(tick, random_action).send()
    except Exception:
        # Handle your exceptions per tick
        pass
