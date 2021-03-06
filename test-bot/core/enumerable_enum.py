class EnumerableEnum:
    @classmethod
    def all(cls):
        return [value for key, value in cls.__dict__.items() if not is_private(key)]


def is_private(key):
    return key.startswith("__") and key.endswith("__")
