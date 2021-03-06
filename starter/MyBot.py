# A base game loop.
# You shouldn't have to modify this file unless you have specific needs.
# Your bot logic should be implemented in bot_logic/bot.
# You can, however, do anything you'd like in here.
# ==============================================================================

from bot_logic.bot import get_bot_name
from bot_logic.bot import get_action
from core.commands import ActionCommand
from core.commands import RegisterBotCommand
from core.logging import configure_file_logging
from core.logging import log
from models.state import State


bot_name = get_bot_name()

print(RegisterBotCommand(bot_name))
bot_id = input()

configure_file_logging(f"MyBot-{bot_id}")
log(f"Bot name is '{bot_name}' with id '{bot_id}'")

while True:
    state = State(input(), bot_id)

    try:
        tick = state.tick
        action = get_action(state)
        print(ActionCommand(tick, action))
    except Exception:
        # Handle your exceptions per tick
        pass
