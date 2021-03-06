import json
from abc import ABC


class JSONSerializable(ABC):
    def __str__(self):
        return json.dumps(self, default=lambda me: me.__dict__, sort_keys=True)
