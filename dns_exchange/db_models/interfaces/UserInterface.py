from abc import ABC


class UserInterface(ABC):
    def __init__(self):
        self.address = ""  # TODO: Generate address
        self.seed_phrase = ""  # TODO: Generate seed_phrase
        self.assets = {}
        self.is_admin = False
