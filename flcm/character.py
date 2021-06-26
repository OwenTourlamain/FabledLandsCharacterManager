import json

from .item import Item
from .exceptions import InventoryFullError
from .constants import Abilities

class AbilitiesContainter:

    def __init__(self, abilities_dict):
        self.charisma = abilities_dict[Abilities.CHARISMA]
        self.combat = abilities_dict[Abilities.COMBAT]
        self.magic = abilities_dict[Abilities.MAGIC]
        self.sanctity = abilities_dict[Abilities.SANCTITY]
        self.scouting = abilities_dict[Abilities.SCOUTING]
        self.thievery = abilities_dict[Abilities.THIEVERY]


class Character:

    def __init__(self, name, profession, rank, abilities, inventory, stamina, shards):

        self.name = name
        self.profession = profession
        self.rank = rank
        self.abilities = AbilitiesContainter(abilities)
        self.inventory = inventory
        self.stamina = stamina
        self.shards = shards


    @property
    def defence(self):
        return self.abilities.combat + self.rank + self.armour


    @property
    def armour(self):
        return self.get_bonus(Abilities.DEFENCE)


    def get_bonus(self, ability):
        bonus = 0
        for item in self.inventory:
            if item.ability == ability:
                if item.value > bonus:
                    bonus = item.value
        return bonus

    def add_item(self, item):
        if len(self.inventory) > 11:
            raise InventoryFullError()
        self.inventory.append(item)
