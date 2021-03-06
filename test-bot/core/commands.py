from abc import ABC, abstractmethod


class Command(ABC):
    def send(self):
        print(self, flush=True)

    @abstractmethod
    def __str__(self) -> str:
        pass


class RegisterBotCommand(Command):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"0:{self.name}"


class ActionCommand(Command):
    def __init__(self, tick, action):
        self.tick = tick
        self.action = action

    def __str__(self):
        return f"{self.tick}:{self.action}"
