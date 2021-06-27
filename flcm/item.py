class Item:

    def __init__(self, name, ability=None, value=None):
        self.name = name
        self.ability = ability
        self.value = value

    def __eq__(self, other):
        if self.name == other.name and self.ability == other.ability and self.value == other.value:
            return True
        return False
